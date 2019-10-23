from socket import *

host = '10.100.93.60'
port = 8899
addr = (host, port)
bufsize = 1024

tcpClient = socket(AF_INET, SOCK_STREAM)  # 这里的参数和UDP不一样。
tcpClient.connect(addr)  # 由于tcp三次握手机制，需要先连接

while True:
    data = input('>>> ').encode(encoding="utf-8")
    if not data:
        break
    # 数据收发和UDP基本一致
    tcpClient.send(data)
    data = tcpClient.recv(bufsize).decode(encoding="utf-8")
    print(data)

tcpClient.close()