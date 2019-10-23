import serial

class Obj_Com(object):

    def __init__(self, com, btl):
        self.ser = serial.Serial(com, btl)


class Com_1(Obj_Com):

    def __init__(self):
        super().__init__("COM4", 115200)


if __name__ == '__main__':
    a = Obj_Com("COM4", 115200)
    abc = Com_1()