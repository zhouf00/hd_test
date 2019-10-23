from socketserver import (TCPServer as TCP, StreamRequestHandler as SRH)  # 可以通过as起别名
from time import ctime

HOST = '127.0.0.1'
PORT = 9999
ADDR = (HOST, PORT)


class MyRequestHandler(SRH):
    def handle(self):
        print('已经连接:', self.client_address)
        self.wfile.write(('[%s] %s' % (ctime(), self.rfile.readline().decode("UTF-8"))).encode("UTF-8"))


tcpServ = TCP(ADDR, MyRequestHandler)
print('等待新的连接。。。。')

tcpServ.serve_forever()  