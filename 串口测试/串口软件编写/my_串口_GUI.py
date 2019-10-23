import wx
import time
import threading
from my_serial import *

ml_list = ['SWA3300-ZJZZ login: ', 'Password: ', 'root@SWA3300-ZJZZ:~# ', "\n"]
info_list =["cat VERSION", "./showid", "./sys_debug dguset", "reboot"]
test_list = ["./sys_debug sysinfo", "./sys_debug sysinfo"]
status_list = ["sys status:SYS_OK", "sys status:SYS_OK"]

class My_Frame(wx.Frame):

    __COM = ["COM4"]
    __BTL = ["115200"]
    ser = ""

    # 开关系列
    __ser_swh = False
    __info_swh = False
    __test_swh = False
    __count_swh = False

    def __init__(self, *args, **kw):
        super(My_Frame, self).__init__(*args, **kw)

        self.SetSize((650, 400))
        self.SetTitle("测试串口")
        self.timer = wx.Timer(self)

        # 画板布局
        self.pnl = wx.Panel(self)
        self.h_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.v1_sizer = wx.BoxSizer(wx.VERTICAL)
        self.v1_h_sizer = wx.BoxSizer(wx.HORIZONTAL)

        # 左边连接模块
        self.lift_box = wx.StaticBoxSizer(wx.StaticBox(self.pnl, 0, label="连接模块"), wx.VERTICAL)
        lift_com_text = wx.StaticText(self.pnl, wx.ID_ANY, "串口号")
        self.lift_box.Add(lift_com_text, 0, wx.EXPAND | wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)
        self.lift_com = wx.Choice(self.pnl, choices=self.__COM)
        self.lift_com.SetSelection(0)
        self.lift_box.Add(self.lift_com, 0, wx.EXPAND | wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)
        lift_btl_text = wx.StaticText(self.pnl, wx.ID_ANY, "比特率")
        self.lift_box.Add(lift_btl_text, 0, wx.EXPAND | wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)
        self.lift_btl = wx.Choice(self.pnl, choices=self.__BTL)
        self.lift_btl.SetSelection(0)
        self.lift_box.Add(self.lift_btl, 0, wx.EXPAND | wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)
        self.lift_button1 = wx.Button(self.pnl)
        self.lift_button1.text = wx.StaticText(self.lift_button1, wx.ID_ANY)
        self.lift_button1.SetForegroundColour("black")
        self.lift_button1.SetLabel("连 接")
        self.lift_box.Add(self.lift_button1, 0, wx.EXPAND | wx.ALIGN_BOTTOM | wx.ALL, 4)
        self.h_sizer.Add(self.lift_box, 0, wx.EXPAND | wx.ALIGN_LEFT | wx.ALL, 5)

        # 中间命令窗口
        self.v1_text_ctrl = wx.TextCtrl(self.pnl, style=wx.TE_RICH | wx.TE_MULTILINE)
        self.v1_sizer.Add(self.v1_text_ctrl, 1, wx.EXPAND | wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)
        self.v1_input_text = wx.TextCtrl(self.pnl)
        self.v1_h_sizer.Add(self.v1_input_text, 1, wx.EXPAND | wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)
        self.v1_input_button = wx.Button(self.pnl,label="发送")
        self.v1_h_sizer.Add(self.v1_input_button, 0, wx.EXPAND | wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)
        self.v1_sizer.Add(self.v1_h_sizer, 0, wx.EXPAND | wx.ALIGN_CENTER_VERTICAL | wx.ALL, 0)
        self.h_sizer.Add(self.v1_sizer, 1, wx.EXPAND | wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)

        # 右边测试模块
        self.right_box = wx.StaticBoxSizer(wx.StaticBox(self.pnl, 0, label="测试模块"), wx.VERTICAL)
        self.right_test_button = wx.Button(self.pnl, label="测试开始")
        self.right_box.Add(self.right_test_button, 0, wx.EXPAND | wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)
        self.right_test_button1 = wx.Button(self.pnl, label="重启")
        self.right_box.Add(self.right_test_button1, 0, wx.EXPAND | wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)
        self.h_sizer.Add(self.right_box, 0, wx.EXPAND | wx.ALIGN_LEFT | wx.ALL, 5)

        self.pnl.SetSizer(self.h_sizer)
        self.Center()
        self.Show()

        # 事件绑定
        self.Bind(wx.EVT_BUTTON, self.con_button, self.lift_button1)
        self.Bind(wx.EVT_BUTTON, self.send_button, self.v1_input_button)
        self.Bind(wx.EVT_BUTTON, self.test_button, self.right_test_button)
        self.Bind(wx.EVT_BUTTON, self.test_reb, self.right_test_button1)

    def con_button(self, e):
        com = self.lift_com.GetStringSelection()
        btl = self.lift_btl.GetStringSelection()
        try:
            self.con_sys(com, btl)
        except Exception as err:
            wx.MessageBox(str(err), "错误", wx.OK | wx.ICON_INFORMATION)

    def send_button(self, e):
        send_str = self.v1_input_text.GetValue()
        self.send_sys_3(send_str)

    def test_button(self, e):
        self.test_sys()

    def send_sys(self, send_str):
        start_time = time.time()
        if self.__ser_swh:
            str = self.ser.data_rec(send_str)
            end_time = time.time()
            print("<%d>%s" % (end_time - start_time, str))
        else:
            wx.MessageBox("串口未连接", "错误", wx.OK | wx.ICON_INFORMATION)

    def send_sys_2(self, send_str):
        start_time = time.time()
        if self.__ser_swh:
            self.ser.data_send(send_str)
            self.ser.data_line()
            end_time = time.time()
            print("<%d>"%(end_time-start_time))
        else:
            wx.MessageBox("串口未连接", "错误", wx.OK | wx.ICON_INFORMATION)

    def send_sys_3(self, send_str):
        start_time = time.time()
        if self.__ser_swh:
            self.ser.data_send(send_str)
            time.sleep(0.1)
            self.ser.data_str(send_str)
            end_time = time.time()
            print("<%d>"%(end_time-start_time))
        else:
            wx.MessageBox("串口未连接", "错误", wx.OK | wx.ICON_INFORMATION)

    def con_sys(self, com, btl):
        if not self.__ser_swh:
            self.ser = Com_Obj(com, btl)
            self.v1_text_ctrl.AppendText("%s连接成功\n"%self.time_now())
            self.lift_button1.SetForegroundColour("red")
            self.lift_button1.SetLabel("断 开")
            self.__ser_swh = True
        else:
            self.lift_button1.SetForegroundColour("black")
            self.lift_button1.SetLabel("连 接")
            self.ser.com_close()
            self.v1_text_ctrl.AppendText("%s已断开\n"%self.time_now())
            self.__ser_swh = False
            self.__info_swh = False
            self.__test_swh = False

    def test_sys(self):
        if not self.__info_swh:
            for i in range(len(info_list)-1):
                self.ser.data_send(info_list[i])
                time.sleep(0.1)
                rec_str = self.ser.data_str(info_list[i])
                self.v1_text_ctrl.AppendText(self.time_now() + rec_str + "\n")
            self.__info_swh = True
        for i in range(len(test_list)):
            self.ser.data_send(test_list[i])
            time.sleep(0.1)
            rec_str = self.ser.data_str(test_list[i])
            if rec_str == status_list[i]:
                print("<%s>:%s" % (self.time_now(), rec_str))
                self.v1_text_ctrl.AppendText(self.time_now() + rec_str + "\n")

    def test_reb(self, e):
        self.ser.data_send("reboot")
        self.ser.data_line()

    def time_now(self):
        return time.strftime('<%H:%M:%S>', time.localtime())


if __name__ == '__main__':
    app = wx.App()
    win = My_Frame(None)
    app.MainLoop()