from socket import *
import sys


HOST = '192.168.1.27'
PORT = 1234
BUFSIZE = 1024
ADDR = (HOST, PORT)

while True:
    tcpCliSock = socket(AF_INET, SOCK_STREAM)
    tcpCliSock.connect(ADDR)
    data = raw_input('>')
    if not data:
        break
    tcpCliSock.send('%s\r\n' % data.encode("UTF-8"))
    data = tcpCliSock.recv(BUFSIZE).decode("UTF-8")
    if not data:
        break
    print(data.strip())
    tcpCliSock.close()