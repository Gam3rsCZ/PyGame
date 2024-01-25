import ast
import sys
import socket
import json
from _thread import start_new_thread

protocol = socket.SOCK_STREAM # UDP SOCK_DGRAM
ipFamily = socket.AF_INET
#serverIP = input("Server IP: ")
#serverPort = int(input("Server port: "))
serverIP = "192.168.1.3"
serverPort = 443

s = socket.socket(ipFamily, protocol)

try:
    s.bind((serverIP, serverPort))
except socket.error as e:
    print(e)
    
s.listen(2) #TCP ONLY
print("Server started\nWaiting for connections\n")

def decodePosition(data:str):#read
    result = json.loads(data)
    return result

def encodePosition(data:dict):#make
    return json.dumps(data)

position = {"Player 1": {"X": 64, "Y": 540}, "Player 2": {"X": 1856, "Y": 540}}

def threadedClient(connection, address, player):
    connection.send(str.encode(encodePosition(json.dumps(position[f"Player {player}"]))))
    reply = ""
    while True:
        try:
            data = decodePosition(connection.recv(1024).decode())
            if data is None:
                # Handle the case where the received data is None
                print("Received None for player position")
                connection.sendall(str.encode(encodePosition({})))
                continue
            position[f"Player {player}"] = data
            
            if not data:
                print("Disconnected\n")
                break
            
            else:
                if player == 1:
                    reply = position["Player 2"]
                else:
                    reply = position["Player 1"]
                print(f"Received: {data}\n")
                print(f"Sending: {reply}\n")
                
            connection.sendall(str.encode(encodePosition(reply)))
        except:
            break
    print(f"Connection to {address[0]} lost\n")
    connection.close()

currentPlayer = 1
while True:
    connection, address = s.accept() # TCP ONLY
    print(f"{address[0]} connected to the server\n")
    
    start_new_thread(threadedClient, (connection, address, currentPlayer))
    currentPlayer += 1