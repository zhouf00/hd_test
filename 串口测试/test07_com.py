import serial
from time import sleep

serialport = serial.Serial("COM3", 115200, timeout=1)
myout = ''
try:
    s = input('input>')
    serialport.write(s.encode('utf-8'))
    sleep(5)
    print('start recive')
    while serialport.inWaiting() > 0:
        myout += serialport.read(1).decode()
    if myout != "":
        print(myout)
        myout = ""
except EnvironmentError as err:
    print(err)
finally:
    serialport.close()
