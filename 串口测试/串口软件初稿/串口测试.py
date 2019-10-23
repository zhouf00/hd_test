import serial
import time
ser = serial.Serial("COM4", 115200, timeout=2)

def abc():
    ser.write("./showid\n".encode())
    time.sleep(0.05)
    num = ser.inWaiting()
    if num:
        print(num)

abc()