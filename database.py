from server import *
import json

class Database:
    def __init__(self, userName, message):
        self.path = r'C:\Users\abhijit Dey\OneDrive\Desktop\Chat Application\database\database.json'
        self.data = {
            'User': userName,
            'Message': message
        }
        with open(self.path, 'r') as readFile:
            self.jsonFile = json.load(readFile)
    
    def store(self):
        if self.data not in self.jsonFile['Messages']:
            self.jsonFile['Messages'].append(self.data)

        with open(self.path, 'w') as dumpFile:
            json.dump(self.jsonFile, dumpFile, indent=1)