import serial


class Com_Obj(object):

    def __init__(self, com, btl):
        self.__ser = []
        self.__com = com
        self.__btl = btl
        self.__ser = serial.Serial(com, btl, timeout=2)

    def con_com(self):
        self.__ser = serial.Serial(self.__com, self.__btl, timeout=2)

    def data_line(self):
        if self.__ser.inWaiting() == 0:
            self.__ser.write("\n".encode())
        rec = self.__ser.readline().decode().split("\r\n")
        return rec

    def log_send(self, str_send):
        if self.__ser.isOpen():
            self.__ser.write((str_send + "\r\n").encode())

    def log_str(self):
        num = self.__ser.inWaiting()
        return self.__ser.read(num).decode().split("\r\n")


    def data_str(self, str_send):
        try:
            num = self.__ser.inWaiting()
            i = 0
            str_list = []
            rec_str = ""
            if num > 0:
                str_list = self.__ser.read(num).decode().split("\r\n")
                print(str_list)
            for var in str_list:
                if var == str_send:
                    rec_str = str_list[i + 1]
                    # print(rec_str)
                i += 1
        except Exception as err:
            return err
        return rec_str

    def data_send(self, str_send):
        if self.__ser.isOpen():
            self.__ser.write((str_send + "\n").encode())

    def open_and_close(self):
        if self.__ser.isOpen():
            return True
        else:
            return False

    def com_close(self):
        if self.__ser.isOpen():
            self.__ser.close()

if __name__ == '__main__':

    myser = Com_Obj("COM3",115200)
    #myser.data_send("reboot")
    myser.data_send('\n')
    a = myser.data_str()
    print(a)
