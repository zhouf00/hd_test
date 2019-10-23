import wx
import time
import threading
from test_2200_v02 import *

ml_list = ['SWA3300-ZJZZ login: ', 'Password: ', 'root@SWA3300-ZJZZ:~# ',"sys status:SYS_OK"]
info_list =["cat VERSION", "./showid", "./sys_debug dguset", "reboot"]
test_list = ["./sys_debug sysinfo"]
status_list = ["sys status:SYS_OK"]


class WorkerThread(threading.Thread):
    """
    This just simulates some long-running task that periodically sends
    a message to the GUI thread.
    """

    def __init__(self, window):
        threading.Thread.__init__(self)
        self.window = window

    def run(self):
        for i in range(1, 51):
            time.sleep(1)
            if i > 60:
                msg = "<%d> 连接服务器有问题"%i
                wx.CallAfter(self.window.LogMessage, msg)
                break
            wx.CallAfter(self.window.LogMessage, msg=i)
        else:
            wx.CallAfter(self.window.thread_finish, self)


class  MyFrame(wx.Frame):

    __COM = ["COM4"]
    __BTL = ["115200"]
    __ser = ""
    __str_cg = "连接成功"
    __count = 0
    __count_ok = 0
    __time_start = 0

    def __init__(self, *args, **kw):
        super(MyFrame, self).__init__(*args, **kw)
        self.threads = []

        self.SetSize((500, 500))
        self.SetTitle("测试串口")
        self.timer = wx.Timer(self) # 创建定时器事件
        self.timeTOcount = 0 # 累计秒数

        self.pnl = wx.Panel(self)
        self.v_sizer = wx.BoxSizer(wx.VERTICAL)
        self.h1_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.h2_sizer = wx.BoxSizer(wx.HORIZONTAL)

        # 命令打印窗口
        self.h1_text = wx.TextCtrl(self.pnl, style=wx.TE_RICH | wx.TE_MULTILINE)
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
        self.h_auto_time = wx.StaticText(self.pnl, label="用时：00")
        self.h_auto_box.Add(self.h_auto_time, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)
        self.h_auto_text = wx.StaticText(self.pnl, label="| Worker Threads: 00")
        self.h_auto_box.Add(self.h_auto_text, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)
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
        self.h3_con_text = wx.StaticText(self.pnl, wx.ID_ANY)
        self.h3_con_text.SetForegroundColour("red")
        self.h3_con_text.SetLabel("未连接")
        self.h3_con_text.Wrap(-1)
        self.h3_box.Add(self.h3_con_text, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)
        self.v_sizer.Add(self.h3_box, 0, wx.EXPAND | wx.ALL, 5)

        self.pnl.SetSizer(self.v_sizer)
        self.Center()
        self.pnl.Fit()
        self.Show()

        # 事件绑定
        self.Bind(wx.EVT_BUTTON, self.h3_button_con, self.h3_button)
        self.Bind(wx.EVT_TIMER, self.timer_test, self.timer)
        self.Bind(wx.EVT_BUTTON, self.start_test, self.h_auto_button1)
        # self.Bind(wx.EVT_CLOSE, self.close_window)
        self.UpdateCount()

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
            self.__time_start = 1
            e.GetEventObject().Disable()

    def start_test(self, e):
        thread = WorkerThread(self)
        self.threads.append(thread)
        self.UpdateCount()
        thread.start()

    def start_test2(self, e):
        self.timer.Start(1000)

    def timer_test(self, e):
        if self.__time_start == 1:
            self.timeTOcount += 1
            self.h_auto_time.SetLabel("用时：%2.d"%self.timeTOcount)
            if self.timeTOcount == 10:
                self.login_sys()
            elif self.timeTOcount == 15:
                self.info_str()
            elif self.timeTOcount == 48:
                self.test_str()


    def close_window(self, e):
        self.stop_threads()
        self.Destroy()

    def stop_threads(self):
        while self.threads:
            thread = self.threads[0]
            self.threads.remove(thread)

    def UpdateCount(self):
        self.h_auto_text.SetLabel("| Worker Thread: %d"%len(self.threads))

    def LogMessage(self, msg):
        self.__ser.open_event()
        self.h_auto_time.SetLabel("用时：%d"%msg)
        if msg == 12:
            self.login_sys()
            self.h1_text.AppendText("登陆成功\n")
        elif msg == 15:
            self.info_str()
        elif msg == 48:
            self.test_str()
            self.__ser.stop_event()

    def thread_finish(self, thread):
        self.threads.remove(thread)
        self.UpdateCount()
        #self.__ser.print_reboot(info_list[-1])
        self.h1_text.AppendText("本次测试结束重启\n")

    def login_sys(self):
        #self.__ser = Com_Obj(self.__COM, self.__BTL)
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
        self.h1_text.AppendText("登陆成功\n")

    def info_str(self):
        i = 0
        while True:
            if i == len(info_list)-1:
                print("%s信息打印完毕%s"%("*"*10,"*"*10))
                break
            else:
                str = self.__ser.print_str(info_list[i])
                i += 1
                rec = "<信息%d>:%s\n"%(i, str)
                #print(rec)
                self.h1_text.AppendText(rec)

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
                        rec = "%s<用时%d>\n"%(str, time_end-time_start)
                        print(rec)
                        self.h1_text.AppendText(rec)
                        self.__count_ok += 1
                        break
                    else:
                        str = self.__ser.print_str(test_list[i])
                        print("<%d>:%s"%(j, str))
                        j += 1
                i += 1
        return self.__count_ok


if __name__ == '__main__':
    app = wx.App()
    win = MyFrame(None)
    app.MainLoop()