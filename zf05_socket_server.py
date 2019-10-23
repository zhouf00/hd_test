import socket

s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
HostPort = ('10.100.93.60',8899)
s.bind(HostPort)  #绑定地址端口
s.listen(5)  #监听最多5个连接请求
while True:
    print('server socket waiting...')
    obj,addr = s.accept()  #阻塞等待链接,创建新链接对象（obj)和客户端地址（addr)
    print('socket object:', obj)
    print('client info:', addr)
    send_data = input(">>>").encode(encoding="utf-8")
    while True:
        client_data = obj.recv(1024)  #通过新链接对象接受数据
        print(client_data)
        obj.send(send_data)  #通过新链接对象发送数据