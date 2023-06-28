from socket import *
import argparse
import threading

MAX_MESSAGE_SIZE = 4096

class Client:
    def __init__(self, options) -> None:
        self.host = options.host
        self.port = options.port
        self.clientSocket = socket(AF_INET, SOCK_STREAM)
        self.clientSocket.connect((self.host, self.port))
        self.nameAuthentication()

    def nameAuthentication(self):
        self.name = input('[+] Enter Username: ')
        self.clientSocket.send(self.name.encode())

    def receiveMessage(self):
        while True:
            try:
                recvMessage = self.clientSocket.recv(MAX_MESSAGE_SIZE).decode()
                if ':' not in recvMessage:
                    print(f'[+] {recvMessage}')
                else:
                    recvMessage = recvMessage.split(':')
                    print(f'[+] {recvMessage[0]}: {recvMessage[1]}')
                
            except:
                break

    def sendMessage(self):
        while True:
            sendMessage = input(f'[{self.name}] -> ')
            if sendMessage == '':
                continue
            else:
                self.clientSocket.send(sendMessage.encode())
                if sendMessage == 'q':
                    self.clientSocket.close()
                    break

    def connection(self):
        recvThread = threading.Thread(target=self.receiveMessage)
        sendThread = threading.Thread(target=self.sendMessage)

        recvThread.start()
        sendThread.start()

        recvThread.join()
        sendThread.join()
                
if __name__ == "__main__":
    desc = 'Clinet Program for the chat Application'
    parser = argparse.ArgumentParser(description=desc)
    parser.add_argument('-n', type=str, default=gethostbyname(gethostname()),
                        dest='host',
                        help='IP of the Chat server %(default)s')
    
    parser.add_argument('-p', type=int, default=8000,
                        dest='port',
                        help='port of the Chat server %(default)s')
    options = parser.parse_args()

    if hasattr(options, '-h'):
        parser.print_help()

    client = Client(options)
    client.connection()