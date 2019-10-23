from socket import *
from time import ctime

ADDR = ("10.100.93.60", 8888)
tcpSer = socket(AF_INET, SOCK_STREAM)

tcpSer.bind(ADDR)
tcpSer.listen(1000)

while True:
    print('waiting for connection ...')
    cli, add = tcpSer.accept()
    print('Got connection from', add)
    while True:
        data = cli.recv(1024).decode('utf-8')
        if not data:
            break
        cli.send('[{}] {}'.format(ctime(), data).encode('utf-8'))

    cli.close()
