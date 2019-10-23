import time
import wx
import serial
from threading import Thread
from wx.lib.pubsub import pub

ml_list = ['SWA3300-ZJZZ login: ', 'Password: ', 'root@SWA3300-ZJZZ:~# ', "V2_1_9_71",
           "The DGU id is 10000009."]

class TestThread(Thread):

    def __init__(self):
        #线程实例化时立即启动
        Thread.__init__(self)
        self.start()
    def run(self):
        #线程执行的代码
        for i in range(10):
            time.sleep(0.03)
            wx.CallAfter(pub.sendMessage, "update")
            time.sleep(0.5)

class MyFrame(wx.Frame):

    # __COM = ["COM1", "COM2", "COM3", "COM4", "COM5", "COM6"]
    # __BTL = ["4800", "9600", "115200"]
    __COM = ["COM3", "COM4"]
    __BTL = ["115200"]

    def __init__(self, *args, **kw):
        super(MyFrame, self).__init__(*args, **kw)

        self.SetSize((500, 400))
        self.SetTitle("测试串口")

        self.pnl = wx.Panel(self)
        self.v_sizer = wx.BoxSizer(wx.VERTICAL)
        self.h1_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.h2_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.h3_sizer = wx.BoxSizer(wx.HORIZONTAL)

        # 命令打印窗口
        self.h1_text = wx.TextCtrl(self.pnl, style=wx.TE_MULTILINE)
        self.h1_sizer.Add(self.h1_text,1, wx.EXPAND | wx.ALL, 5)
        self.v_sizer.Add(self.h1_sizer, 1, wx.EXPAND | wx.ALL, 5)

        # 发送命令
        self.h2_text = wx.TextCtrl(self.pnl)
        self.h2_sizer.Add(self.h2_text, 1, wx.EXPAND | wx.ALL, 5)
        self.h2_button = wx.Button(self.pnl, label="发 送")
        self.h2_sizer.Add(self.h2_button, 0, wx.EXPAND | wx.ALL, 5)
        self.v_sizer.Add(self.h2_sizer, 0, wx.EXPAND | wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)

        # 连接模块
        self.h3_box = wx.StaticBoxSizer(wx.StaticBox(self.pnl, 0, label="串口连接"), wx.HORIZONTAL)
        h3_com_text = wx.StaticText(self.pnl, wx.ID_ANY, "串口号")
        self.h3_box.Add(h3_com_text, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)
        self.h3_com_choice = wx.Choice(self.pnl, choices=self.__COM)
        self.h3_com_choice.SetSelection(0)
        self.h3_box.Add(self.h3_com_choice, 0, wx.EXPAND | wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)
        h3_btl_text = wx.StaticText(self.pnl, wx.ID_ANY, "波特率")
        self.h3_box.Add(h3_btl_text, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)
        self.h3_btl_choice = wx.Choice(self.pnl, choices=self.__BTL)
        self.h3_btl_choice.SetSelection(0)
        self.h3_box.Add(self.h3_btl_choice, 0, wx.EXPAND | wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)
        self.h3_button = wx.Button(self.pnl, label="连接")
        self.h3_box.Add(self.h3_button, 0, wx.EXPAND | wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)
        self.v_sizer.Add(self.h3_box, 0, wx.EXPAND | wx.ALL, 5)

        self.pnl.SetSizer(self.v_sizer)
        self.Center()
        self.pnl.Fit()
        self.Show()

        # 事件绑定
        self.Bind(wx.EVT_BUTTON, self.send_data, self.h2_button)
        self.Bind(wx.EVT_BUTTON, self.h3_button_con, self.h3_button)

        #pub.subscribe(self.receive_data, "update")

    def send_data(self, e):
        # TestThread()
        send_str = self.h2_text.GetValue()
        self.ser.write((send_str+"\n").encode())
        self.h1_text.AppendText("发送:" + send_str + "\n")
        rec_all = self.ser.readall().decode()
        rec_list = rec_all.split("\r\n")
        i = 0
        for var in rec_list:
            print("<%d>:%s"%(i, var))
            if var == send_str:
                self.h1_text.AppendText("收到:" + rec_list[i+1] + "\n")
            i += 1

    def h3_button_con(self, e):
        com = self.h3_com_choice.GetStringSelection()
        btl = self.h3_btl_choice.GetStringSelection()
        try:
            self.ser = self.con_host(com, btl)
            print(self.ser)
        except Exception as err:
            print(err)
            wx.MessageBox(str(err),"错误", wx.OK | wx.ICON_INFORMATION)
        else:
            # 关闭按键
            e.GetEventObject().Disable()

    def con_host(self, com, btl):
        return serial.Serial(com, btl, timeout=1)

    def receive_data(self):
        res = self.ser.readline().decode()
        if len(res) != 0:
            print("%s<%d>"%(res.strip(),len(res)))
            if res in ml_list:
                self.h1_text.AppendText("re:" + res.strip() + "\n")

if __name__ == '__main__':
    app = wx.App()
    win = MyFrame(None)
    app.MainLoop()