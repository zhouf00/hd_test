import wx
import time
import threading
#from my_serial import *

ml_list = ['SWA3300-ZJZZ login: ', 'Password: ', 'root@SWA3300-ZJZZ:~# ']
user_list = ["root"]
info_list =["cat VERSION", "./showid", "./sys_debug dguset"]
test_list = ["./sys_debug sysinfo", "cat VERSION"]
status_list = ["sys status:SYS_OK", "V2_1_11_91"]


class WorkerThread(threading.Thread):
    """
    This just simulates some long-running task that periodically sends
    a message to the GUI thread.
    """
    def __init__(self, window):
        threading.Thread.__init__(self)
        self.window = window
        self.__flag = threading.Event()
        self.__flag.set()
        self._running = True

    def run(self):
        while self._running and self.window.thread_count > 0:
            self.__flag.wait()
            print("**********进程中**********")
            if self.window.reboot_status:
                time.sleep(0.5)
                wx.CallAfter(self.window.reboot_sys)
            elif self.window.login_status:
                wx.CallAfter(self.window.login_sys)
                time.sleep(0.5)
            elif self.window.test_swh:
                wx.CallAfter(self.window.test_info)
                time.sleep(0.5)
                wx.CallAfter(self.window.test_func)
            else:
                wx.CallAfter(self.window.init_val)
                self.window.thread_count -= 1
                print(self.window.thread_count)
        wx.CallAfter(self.window.test_flag)
        print("测试结束")


    def stop(self):
        self._running = False

    def setFlag(self, parm):
        if parm:
            self.__flag.set()
        else:
            self.__flag.clear()


class My_Frame(wx.Frame):

    __COM = ["COM4"]
    __BTL = ["115200"]
    __COUNT = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "20"]
    __ERR = 5
    ser = ""

    # 开关系列
    __ser_swh = False
    __info_swh = False
    __thread_swh = False
    test_swh = False
    __count_swh = False
    reboot_status = True
    login_status = True

    def __init__(self, *args, **kw):
        super(My_Frame, self).__init__(*args, **kw)

        self.SetSize((750, 400))
        self.SetTitle("测试串口")
        self.timer = wx.Timer(self)
        self.threads = []   # 线程数量

        # 值初始化
        self.thread = ""
        self.reboot_str = ""
        self.thread_count = 1
        self.info_index = 0
        self.func_index = 0
        self.func_err = 1
        self.info_err = 1


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
        self.right_count = wx.Choice(self.pnl, choices=self.__COUNT)
        self.right_count.SetSelection(0)
        self.right_box.Add(self.right_count, 0, wx.EXPAND | wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)
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
        #self.Bind(wx.EVT_CLOSE, self.window_close)
        #self.Bind(wx.EVT_BUTTON, self.test_button, self.right_test_button1)

        # 创建主线程
        self.thread = WorkerThread(self)
        self.thread.setDaemon(True)

    # 连接按键
    def con_button(self, e):
        com = self.lift_com.GetStringSelection()
        btl = self.lift_btl.GetStringSelection()
        try:
            self.con_sys(com, btl)
        except Exception as err:
            wx.MessageBox(str(err), "错误", wx.OK | wx.ICON_INFORMATION)

    # 发送按键
    def send_button(self, e):
        send_str = self.v1_input_text.GetValue()
        self.send_sys(send_str)

    # 测试按键
    def test_button(self, e):
        self.thread_count = int(self.right_count.GetStringSelection())
        self.init_val()
        if not self.__thread_swh:
            #self.thread = WorkerThread(self)
            self.thread.start()
            self.__thread_swh = True
            self.v1_text_ctrl.AppendText("%s测试开始\n" % self.time_now())
        else:
            self.thread.stop()
            self.__thread_swh = False
            self.v1_text_ctrl.AppendText("%s测试停止\n" % self.time_now())

    # 重启按键
    def test_reb(self, e):
        self.ser.data_send("reboot")
        self.ser.data_line()

    # 窗口命令发送
    def send_sys(self, send_str):
        if self.__ser_swh:
            self.ser.data_send(send_str)
            time.sleep(0.1)
            rec = self.ser.data_str(send_str)
            self.v1_text_ctrl.AppendText(self.time_now() + rec + "\n")
        else:
            wx.MessageBox("串口未连接", "错误", wx.OK | wx.ICON_INFORMATION)

    # 连接系统
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
            self.init_val()

    # 系统启动功能
    def reboot_sys(self):
        self.thread.setFlag(False)
        print("<<启动函数>>")
        rec = self.ser.data_line()
        if rec[0] in ml_list:
            if rec[0] == ml_list[0]:
                self.reboot_str = rec[0]
            else:
                self.reboot_str = rec[0]
            self.reboot_status = False
            print("%s<退出启动函数>"%self.reboot_str)
            self.thread.setFlag(True)
            return
        else:
            #print("%s>>重启函数"%rec)
            self.thread.setFlag(True)

    # 登陆功能
    def login_sys(self):
        self.thread.setFlag(False)
        print("<<登陆函数>>")
        if self.reboot_str == ml_list[0]:
            self.ser.log_send("root")
            time.sleep(0.2)
            rec = self.ser.log_str()
            print(rec)
            if rec[-1] == ml_list[1] or rec[-2] == ml_list[1]:
                self.ser.log_send("root")
                time.sleep(0.2)
                rec = self.ser.log_str()
                self.login_status = False
                print("%s<退出登陆函数1>" % rec)
                self.thread.setFlag(True)
                return
        elif self.reboot_str == ml_list[2]:
            self.login_status = False
            time.sleep(0.2)
            rec = self.ser.log_str()
            print("%s<退出登陆函数2>" %rec)
            self.thread.setFlag(True)
            return
        else:
            self.ser.log_send("")
            self.thread.setFlag(True)

    # 信息输入及功能测试命令输入
    def test_info(self):
        self.thread_pause()
        if self.info_index < len(info_list):
            rec = self.ser.data_send(info_list[self.info_index])
        else:
            if self.func_index == len(test_list):
                self.thread_resume()
                return
            rec =self.ser.data_send(test_list[self.func_index])
        self.thread_resume()
        return rec

    # 信息输出及功能测试结果输出
    def test_func(self):
        self.thread_pause()
        if self.info_index < len(info_list):
            rec = self.ser.data_str(info_list[self.info_index])
            if rec[-5:] == "error":
                self.info_err += 1
                if self.info_err > self.__ERR:
                    print("info is error")
                    self.info_err = 1
                    self.info_index += 1
            else:
                self.info_index += 1
        else:
            if self.func_index == len(test_list):
                self.test_swh = False
                #self.ser.data_send("reboot")
                self.thread_resume()
                return
            rec = self.ser.data_str(test_list[self.func_index])
            if rec != status_list[self.func_index]:
                self.func_err += 1
                if self.func_err > self.__ERR:
                    print("func is error")
                    self.func_err = 1
                    self.func_index += 1
                    self.thread_resume()
                    return
            else:
                self.func_index += 1
        self.v1_text_ctrl.AppendText(self.time_now() + rec + "\n")
        self.thread_resume()
        return rec

    # 测试数据，开关初始化
    def init_val(self):
        self.thread_pause()
        self.reboot_str = ""
        self.info_index = 0
        self.func_index = 0
        self.func_err = 1
        self.info_err = 1
        self.test_swh = True
        self.__info_swh = False
        self.login_status = True
        self.reboot_status = True
        self.thread_resume()

    def test_flag(self):
        self.__thread_swh = False

    def thread_pause(self):
        self.thread.setFlag(False)

    def thread_resume(self):
        self.thread.setFlag(True)

    def time_now(self):
        return time.strftime('<%H:%M:%S>', time.localtime())


if __name__ == '__main__':
    app = wx.App()
    win = My_Frame(None)
    app.MainLoop()