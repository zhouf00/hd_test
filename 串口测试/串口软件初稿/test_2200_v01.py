import time
import serial

ml_list = ['SWA3300-ZJZZ login: ', 'Password: ', 'root@SWA3300-ZJZZ:~# ', "V2_1_9_71",
           "The DGU id is 10000009."]

in_list =[" ", "root", "cat VERSION", "./showid", "./sys_debug dguset", "./sys_debug sysinfo"]


def con_to_com(com, btl):
    return serial.Serial(com, btl, timeout=1)

def to_list(from_ser):
    return from_ser.split("\r\n")

def test_obj(ser, send_str, count = 1):
    rec_list = to_list(ser.readall().decode())
    #print("<%d>:%s"%(len(rec_list),rec_list))
    i = 0
    for var in rec_list:
        #print("<%d>%s"%(i,var))
        if var == send_str:
            print("<%d>:%s"%(i,rec_list[i+1]))
    return rec_list[-1]


if __name__ == '__main__':
    COM = "COM4"
    BTL = "115200"
    ser = con_to_com(COM, BTL)
    i = 0
    j = 1
    rec = ""
    while True:
        if i == 0:
            str = in_list[0]
            ser.write((str + "\n").encode())
            rec = test_obj(ser, str)
            i += 1
        if j == len(in_list)-1:
            print("添加完成")
            break
        if rec == ml_list[0]:
            str = in_list[1]
            ser.write((str + "\n").encode())
            rec = test_obj(ser, str)
        elif rec == ml_list[1]:
            str = in_list[1]
            ser.write((str + "\n").encode())
            rec = test_obj(ser, str)
        elif rec == ml_list[2]:
            str = in_list[j+1]
            ser.write((str + "\n").encode())
            rec = test_obj(ser, str)
            j += 1

