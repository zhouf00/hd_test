import wx
import time
from 串口软件.test_2200_v02 import *

ml_list = ['SWA3300-ZJZZ login: ', 'Password: ', 'root@SWA3300-ZJZZ:~# ',"sys status:SYS_OK"]
info_list =["cat VERSION", "./showid", "./sys_debug dguset", "reboot"]
test_list = ["./sys_debug sysinfo"]
status_list = ["sys status:SYS_OK"]

class  MyFrame(wx.Frame):

    __COM = ["COM3", "COM4"]
    __BTL = ["115200"]
    __ser = ""
    __str_cg = "连接成功"

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
        self.h3_con_text = wx.StaticText(self.pnl, wx.ID_ANY)
        self.h3_con_text.SetForegroundColour("red")
        self.h3_con_text.SetLabel("未连接")
        self.h3_con_text.Wrap(-1)
        self.h3_box.Add(self.h3_con_text, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)

        self.pnl.SetSizer(self.v_sizer)
        self.Center()
        self.pnl.Fit()
        self.Show()

        # 事件绑定
        self.Bind(wx.EVT_BUTTON, self.h3_button_con, self.h3_button)
        self.Bind(wx.EVT_BUTTON, self.auto_test, self.h2_button)

    def h3_button_con(self, e):
        com = self.h3_com_choice.GetStringSelection()
        btl = self.h3_btl_choice.GetStringSelection()
        try:
            self.__ser = Com_Obj(com, btl)
        except Exception as err:
            print(err)
            wx.MessageBox(str(err),"错误", wx.OK | wx.ICON_INFORMATION)
        else:
            # 关闭按键
            self.h3_con_text.SetForegroundColour("green")
            self.h3_con_text.SetLabel("连接成功")
            e.GetEventObject().Disable()

    def auto_test(self, e):
        count = 2
        i = 0
        while True:
            if i > 0:
                pass
            self.login_sys()
            #time.sleep(10)
            self.info_str()
            self.test_str()
            i += 1
            if i < count:
                self.__ser.print_reboot(info_list[-1])
                self.__ser.stop_event()
                print("测试结束重启****")
            else:
                break
        print("共测试<%d>次"%count)

    def login_sys(self):
        str = self.__ser.print_end_str(" ")
        i = 0
        while True:
            if str == ml_list[2]:
                #print(str)
                break
            elif str == ml_list[0] or str == ml_list[1]:
                print("<%d>:%s" % (i, str))
                str = self.__ser.print_end_str("root")
            else :
                #print("<%d>:%s"%(i,str))
                str = self.__ser.print_end_str(" ")
            i += 1

    def info_str(self):
        i = 0
        while True:
            if i == len(info_list)-1:
                print("%s信息打印完毕%s"%("*"*10,"*"*10))
                break
            else:
                str = self.__ser.print_str(info_list[i])
                i += 1
                print("<测试%d>:%s"%(i, str))

    def test_str(self):
        i = 0
        while True:
            if i == len(test_list):
                print("%s测试结束%s" % ("*" * 10, "*" * 10))
                break
            else:
                print("功能测试开始")
                str = self.__ser.print_str(test_list[i])
                time_start = time.time()
                j = 0
                while True:
                    if str == status_list[i]:
                        time_end=time.time()
                        print("%s<用时%d>"%(str, time_end-time_start))
                        break
                    else:
                        str = self.__ser.print_str(test_list[i])
                        print("<%d>:%s"%(j, str))
                        j += 1
                i += 1


if __name__ == '__main__':
    app = wx.App()
    win = MyFrame(None)
    app.MainLoop()