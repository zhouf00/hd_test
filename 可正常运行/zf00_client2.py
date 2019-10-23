from socket import *

HOST = "10.100.93.60"
PORT = 8888
ADDR = (HOST, PORT)

cliSocket = socket(AF_INET, SOCK_STREAM)
cliSocket.connect(ADDR)

while True:
    data = input('> ')
    if not data:
        break
    cliSocket.send(data.encode('utf-8'))
    data = cliSocket.recv(1024).decode('utf-8')
    if not data:
        break
    print(data)

cliSocket.close()
