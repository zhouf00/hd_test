import serial, time
from serial.tools import list_ports

# 检查电脑的COM口
plist = list(list_ports.comports())
for var in plist:
    print(var)

def com_print(w='\n'):
    print('写入打印', com.write(w.encode()))
    i = 1
    while True:
        #time.sleep(0.02)
        com.inWaiting()
        res = com.readline().decode()
        print("<%s>循环" % i, res)
        if res.find('SWA3300-ZJZZ login:') != -1:
            print('返回值打印', res)
            print('写入打印', com.write('root\n'.encode()))
        elif res.find('Password:') != -1:
            print('返回值打印', res)
            print('写入打印', com.write('root\n'.encode()))
        elif res.find('root@SWA3300-ZJZZ:') != -1:
            print(res)
            break
        i+=1


def com_reboot():
    com_print()
    print('写入打印', com.write('reboot\n'.encode()))
    i = 1
    while True:
        #time.sleep(0.02)
        com.inWaiting()
        res = com.readline()
        print("<%s>循环" % i, type(res), res)
        # print(res == 'Press qw to cmdline...Booting from nand ...\r\n'.encode())
        #if res != 'Press qw to cmdline...Booting from nand ...\r\n'.encode():
        if res == '\r\n'.encode():
            print(res)
            print('写入打印', com.write('qwqwqwqwqw'.encode()))
        elif res == 'Press qw to cmdline...Sanway@335x->qwqwqwqwqwqwqwqwqwqwqwqwqwqw'.encode():
            print('写入打印', com.write('\n'.encode()))
        i+=1

def com_ifconfig():
    com_print()
    #print('写入打印', com.write((ip+'\n').encode()))
    print('写入打印', com.write('ifconfig\n'.encode()))
    while True:
        res = com.readline().decode()
        if res.find('addr:') != -1:
            print(res)
            hostip = res.split(' ')
            print(hostip)
            hostip = hostip[hostip.index('inet')+1].split(':')[1]
            print(hostip)
        elif res.find('root@SWA3300-ZJZZ:~#') != -1:
            print(res)
            break

def com_change_ip(ip):
    com_print()
    print('写入打印', com.write((ip+'\n').encode()))

def com_comm(comm):
    com_print()
    print('写入打印', com.write('cd /work/data\n'.encode()))
    print('写入打印', com.write(('./deploy2.sh ' + comm + '\n').encode()))
    com_print()
    #print('写入打印', com.write('reboot\n'.encode()))


if __name__ == '__main__':

    com = serial.Serial('com3', 115200, timeout=30)
    print(com)
    #com_print()
    #com_reboot()
    # com_ifconfig()
    comm = input("请输入DGMID:")
    com_comm(comm)
    com.close()

# while True:
#     time.sleep(0.05)
#     num = com.inWaiting()
#     res = com.read(num).decode()
#     # res = com.read(num).decode().split('\r\n')
#     print('返回值打印',res)
#     print('写入qw打印', com.write('qw\n'.encode()))


# "Press qw to cmdline"
# "b'Press qw to cmdline...Sanway@335x->qwqwqwqwqwqwqwqwqwqwqwqwqwqw'"
# "b'Press qw to cmdline...Sanway@335x->qwqwqwqwqwqwqwqwqwqwqwqwqwqw'"