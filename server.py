from socket import *
import threading
import argparse
import logging
import os

from database import Database

MAX_MESSAGE_SIZE = 4096

class StaticResponse:
    response = b'Name is already in use by other perticipants!'

class ChatRoom:
    def __init__(self) -> None:
        self.participants = {}
    
    def addParticapants(self, name, connection):
        setOption = self.options()
        if name not in self.participants:
            self.participants[name] = connection
            connection.send(f'Welcome to the Chat Room\n{setOption}\n'.encode())
            self.broadcast(name, ' Joined the Chat!')
        else:
            connection.send(StaticResponse.response)
            connection.close()

    def removeParticipants(self, clientName):
        if clientName in self.participants:
            del self.participants[clientName]

    def broadcast(self, clietName, recvMessage):
        for name, connection in self.participants.items():
            if name != clietName:
                connection.send(f'{clietName}:{recvMessage}'.encode())

    def options(self):
        desc = f'''[+] To View Participents -> view\n[+] To Quit Chat, press -> q\n'''
        return desc
    
    def viewParticipants(self):
        listOfParticipants = list(self.participants.keys())
        formatParticipants = ''
        for participants in listOfParticipants:
            formatParticipants += f'{participants}, '
        return formatParticipants[:-2]

class ConnectionHandling:
    def __init__(self, clientCon:socket, chatRoom:ChatRoom):
        self.clientConnection = clientCon
        self.chatRoom = chatRoom
        self.serve()
    
    def serve(self):
        nameOfClient = self.clientConnection.recv(MAX_MESSAGE_SIZE).decode()
        
        self.chatRoom.addParticapants(nameOfClient, self.clientConnection)

        while True:
            recvMessage = self.clientConnection.recv(MAX_MESSAGE_SIZE).decode()

            if recvMessage == 'q':
                self.chatRoom.removeParticipants(nameOfClient)
                self.chatRoom.broadcast(nameOfClient, ' Left the Chat!')
                self.clientConnection.close()
                break

            elif recvMessage == 'view':
                participantList = self.chatRoom.viewParticipants()
                self.clientConnection.send(participantList.encode())
            else:
                self.chatRoom.broadcast(nameOfClient, recvMessage) 
                data = Database(nameOfClient, recvMessage)
                data.store()

class Server:
    def __init__(self, options) -> None:
        print('Server is listning...')
        self.host = options.host
        self.port = options.port
        self.serverSocket = socket(AF_INET, SOCK_STREAM)
        self.serverSocket.bind((self.host, self.port))
        self.serverSocket.listen(20)
        print(f"Listening at: http://{self.host}:{self.port}") # will be changed
        self.chatRoom = ChatRoom()

    def start(self):
        while True:
            clientCon, addr = self.serverSocket.accept()
            print(addr)
            thread = threading.Thread(target=ConnectionHandling, args=(clientCon, self.chatRoom))
            thread.start()

class ArgumentParsing:
    def __init__(self):
        desc = 'Python Chat Room - Multithreaded'
        parser = argparse.ArgumentParser(description=desc)
        parser.add_argument('-n', type=str, default=gethostbyname(gethostname()),
                            dest='host',
                            help='Specify host IP where server will be hosted. ex. %(default)s')
        parser.add_argument('-p', type=int, default=8000, dest='port',
                            help='Specify the port number where the server process will listin. ex. %(default)s')
        
        self.options = parser.parse_args()

        if hasattr(self.options, '-h'):
            parser.print_help()