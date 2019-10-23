import serial

# 打开串口
serialPort = "COM3"  # 串口
baudRate = 115200  # 波特率
ser = serial.Serial(serialPort, baudRate, timeout=0.5)
input_s = input("请输入命令：")
send_list = []
input_s = (input_s + '\r\n').encode('utf-8')
ser.write(input_s)
num = ser.inWaiting()
data = ser.read(num)
num = len(data)
data.decode('utf-8')