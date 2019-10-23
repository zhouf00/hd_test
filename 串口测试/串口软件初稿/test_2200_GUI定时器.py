import wx
import time
#from 串口软件.test_2200_v02 import *

ml_list = ['SWA3300-ZJZZ login: ', 'Password: ', 'root@SWA3300-ZJZZ:~# ']
info_list =["cat VERSION", "./showid", "./sys_debug dguset", "reboot"]
test_list = ["./sys_debug sysinfo"]
status_list = ["sys status:SYS_OK"]

class  MyFrame(wx.Frame):

    __COM = ["COM4"]
    __BTL = ["115200"]
    __ser = ""
    __str_cg = "连接成功"
    __time_star = False
    __choice_list = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "20", "30"]

    def __init__(self, *args, **kw):
        super(MyFrame, self).__init__(*args, **kw)

        self.SetSize((500, 400))
        self.SetTitle("测试串口")
        self.timer = wx.Timer(self)

        # 变量初始化
        self.time_count = 0
        self.test_login = 1002
        self.test_info = 0
        self.test_func = 0
        self.str = " "
        self.index_info = 0
        self.index_test = 0
        self.tmp_time = 0
        self.test_count = 0

        self.pnl = wx.Panel(self)
        self.hw_sizer = wx.BoxSizer(wx.HORIZONTAL)
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

        # 自动测试模块
        self.h_auto_box = wx.StaticBoxSizer(wx.StaticBox(self.pnl, 0, label="自动测试"), wx.HORIZONTAL)
        self.h_auto_button1 = wx.Button(self.pnl, label="测试")
        self.h_auto_box.Add(self.h_auto_button1, 0, wx.EXPAND | wx.ALL, 5)
        self.h_auto_chioce = wx.Choice(self.pnl, choices=self.__choice_list)
        self.h_auto_chioce.SetSelection(0)
        self.h_auto_box.Add(self.h_auto_chioce, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)
        self.v_sizer.Add(self.h_auto_box, 0, wx.EXPAND | wx.ALL, 5)

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
        self.Bind(wx.EVT_BUTTON, self.auto_start, self.h_auto_button1)
        self.Bind(wx.EVT_TIMER, self.auto_test, self.timer)

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
            self.__time_star = True
            e.GetEventObject().Disable()

    def auto_start(self, e):
        self.timer.Start(1000)
        self.h_auto_button1.Disable()

    def auto_test(self, e):
        if not self.__time_star or self.test_count == int(self.h_auto_chioce.GetStringSelection()):
            self.time_stop()
        else: #self.__time_star and self.test_count < int(self.h_auto_chioce.GetStringSelection()):
            self.time_count += 1
            if self.test_login == 1002 or self.test_login == 1000:
                self.test_login = self.login_sys()
            elif self.test_login == 1001 and self.test_info != 1003:
                self.test_info = self.info_str()
            elif self.test_info == 1003 and self.test_func != 1005:
                self.test_func = self.test_str()
            elif self.test_func == 1005 and self.index_test == len(test_list) and self.tmp_time == 0:
                self.__ser.print_reboot(info_list[-1])
                self.tmp_time = self.time_count + 30
                self.h1_text.AppendText("%s正在重启.....\n"%self.time_now())
            elif self.time_count == self.tmp_time:
                self.init_str()
                self.test_count += 1
                #self.time_stop()
                print("<%d>重启成功"%(self.time_count,))
                self.h1_text.AppendText("%s重启成功\n"%self.time_now())
            #print("<%d>login:%d,info:%d, test:%d"%(self.time_count,self.test_login,self.test_info,self.test_func))
            if self.time_count != 0:
                print("<%d>" % (self.time_count))

    def login_sys(self):
        if self.str == ml_list[2]:
            self.h1_text.AppendText("%s登陆成功\n"%self.time_now())
            return 1001
        elif self.str == ml_list[0] or self.str == ml_list[1]:
            self.str = self.__ser.print_end_str("root")
            return 1000
        else :
            self.str = self.__ser.print_end_str(" ")
            return 1002

    def info_str(self):
        if self.index_info == len(info_list)-1:
            print("%s信息打印完毕%s"%("*"*10,"*"*10))
            return 1003
        else:
            str = self.__ser.print_str(info_list[self.index_info])
            self.index_info += 1
            print("<%s>:%s"%(self.time_now(), str))
            self.h1_text.AppendText((self.time_now() + str + "\n"))

    def test_str(self):
        if self.index_test == len(test_list):
            print("%s测试结束%s" % ("*" * 10, "*" * 10))
            return 1005
        else:
            str = self.__ser.print_str(test_list[self.index_test])
            if str == status_list[self.index_test]:
                print("<%s>:%s" % (self.time_now(), str))
                self.h1_text.AppendText((self.time_now() + str + "\n"))
                self.index_test += 1
            else:
                str = self.__ser.print_str(test_list[self.index_test])
                print("<%s>:%s"%(self.time_now(),str))
                self.h1_text.AppendText((self.time_now() + str + "\n"))

    def init_str(self):
        self.test_login = 1002
        self.test_info = 0
        self.test_func = 0
        self.time_count = 0
        self.str = " "
        self.index_test = 0
        self.index_info = 0
        self.tmp_time = 0

    def time_now(self):
        return time.strftime('<%H:%M:%S>', time.localtime())

    def time_stop(self):
        self.test_count = 0
        self.timer.Stop()
        self.h_auto_button1.Enable()



if __name__ == '__main__':
    app = wx.App()
    win = MyFrame(None)
    app.MainLoop()