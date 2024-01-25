import socket

class Network():
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.serverIP = "192.168.1.3"
        self.serverPort = 443
        self.serverAddress = (self.serverIP, self.serverPort)
        self.position = self.connect()
        
    def connect(self):
        try:
            self.client.connect(self.serverAddress)
            return self.client.recv(1024).decode()
        except:
            pass
    
    def send(self, data):
        try:
            self.client.send(str.encode(data))
            return self.client.recv(1024).decode()
        except socket.error as e:
            print(e)

    def getPosition(self):
        return self.position