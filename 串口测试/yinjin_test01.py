import serial
import time

# 打开串口
serialPort = "COM3"  # 串口
baudRate = 115200  # 波特率
ml_list = ['SWA3300-ZJZZ login: ', 'Password: ', 'root@SWA3300-ZJZZ:~# ']

def test01():
    i = 0
    ser = serial.Serial(serialPort, baudRate, timeout=1)
    ser.write("\n".encode())
    while True:
        index = 0
        sec_list = ser.readall().decode().split("\r\n")
        if sec_list[-1] == ml_list[2]:
            if test_ml(i) == 0:
                return print("测试结束")
            ser.write((test_ml(i) + "\n").encode())
            new_sec = ser.readall().decode().split("\r\n")
            for var in new_sec:
                if var == test_ml(i):
                    print("<%d>%s"%(i,var))
                    print("<%d>结束为：%s"%(i,new_sec[index+1]))
                    i += 1
                    break
        elif sec_list[-1] == ml_list[0]:
            ser.write("root\n".encode())
        elif sec_list[-1] == ml_list[1]:
            ser.write("root\n".encode())
        else:
            ser.write("\n".encode())

def test_ml(count):
    my_list = ["cat VERSION", "./showid", ""]
    if count == len(my_list):
        return 0
    else:
        return my_list[count]


if __name__ == '__main__':
    test01()
