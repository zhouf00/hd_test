import serial


class Com_Obj(object):

    def __init__(self, com, btl):
        self.ser = serial.Serial(com, btl, timeout=1)

    def to_list(self):
        rec = self.ser.readall().decode()
        return rec.split("\r\n")

    def print_str(self, send_str):
        self.ser.write((send_str + "\n").encode())
        rec_str = ""
        rec_list = self.to_list()
        i = 0
        for var in rec_list:
            if var == send_str:
                rec_str = rec_list[i+1]
                #print("<%d>:%s"%(i, rec_str))
            i += 1
        return rec_str

    def print_end_str(self,send_str):
        self.ser.write((send_str + "\n").encode())
        rec_list = self.to_list()
        return rec_list[-1]

    def print_reboot(self, send_str):
        self.ser.write((send_str + "\n").encode())

    def stop_event(self):
        if self.ser.isOpen():
            self.ser.close()

    def open_event(self):
        if not self.ser.isOpen():
            self.ser.open()

    def test(self):
        self.ser.isOpen()
        self.ser.is_open()