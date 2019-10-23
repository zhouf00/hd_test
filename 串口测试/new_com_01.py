import serial
import time
import threading


class ComThread(object):

    def __init__(self, com, btl):
        self.ser = None
        self.alive = False
        self.waitEnd = None
        self.port = com
        self.btl = btl
        self.ID = None
        self.Data = None

    def waiting(self):
        if not self.waitEnd is None:
            self.waitEnd.wait()

    def setstop_event(self):
        if not self.waitEnd is None:
            self.waitEnd.set()
        self.alive = False
        self.stop()

    def start(self):
        self.ser = serial.Serial(self.port, self.btl, timeout=2)
        self.ser.open()
        if self.ser.is_open():
            self.waitEnd = threading.Event()
            self.alive = True
            self.thread_read = None
            self.thread_read = threading.Thread(target = self.reader)
            self.thread_read.setDaemon(1)
            self.thread_read.start()
            return True
        else:
            return False

    def send_Data(self, i_msg, send):
        lmsg = ""
        isOK = False
        if isinstance(i_msg):
            lmsg = i_msg.encode()
        else:
            lmsg = i_msg
        try:
            self.ser.write(send)
        except Exception as ex:
            pass
        return isOK

    def reader(self):
        while self.alive:
            time.sleep(0.1)

            data = ""
            data = data.encode()

            n = self.ser.inWaiting()
            if n:
                data = data + self.ser.read(n)
                print("get data from serial port:",data)
                print(type(data))

            n = self.ser.inWaiting()


if __name__ == '__main__':
    pass