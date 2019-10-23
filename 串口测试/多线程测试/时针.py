import wx
import time
import wx.gizmos as gizmos

ICON_START = '|>'
ICON_SUSPEND = '||'
ICON_RESTART = '<|'
TIMETOCOUNT = 40 * 60


class ClockWindow(wx.Window):
    """LED CLOCK"""

    def __init__(self, parent=None, id=-1):
        wx.Window.__init__(self, parent, id, size=(258, 92))
        # wx.Window.__init__(self, parent, id, size=sz)
        self.parent = parent

        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.timer = wx.Timer(self)  # 创建定时器
        self.Bind(wx.EVT_TIMER, self.OnTimer, self.timer)  # 绑定一个定时器事件
        self.timeToCount = 0  # 累计秒数
        w, h = self.GetClientSize()
        # print w,h
        self.led = gizmos.LEDNumberCtrl(self, -1, wx.DefaultPosition, (w - 10, h - 30), gizmos.LED_ALIGN_CENTER)
        self.led.SetBackgroundColour("black")
        self.led.SetForegroundColour("red")

        # 开始按钮
        self.startButton = wx.Button(self, id, label=ICON_START)
        self.startButton.SetToolTip(wx.ToolTip('Start'))
        self.Bind(wx.EVT_BUTTON, self.OnStart, self.startButton)

        # 暂停按钮
        self.suspendButton = wx.Button(self, id, label=ICON_SUSPEND)
        self.suspendButton.SetToolTip(wx.ToolTip('Suspend'))
        self.Bind(wx.EVT_BUTTON, self.OnStop, self.suspendButton)

        # 重新开始按钮
        self.restartButton = wx.Button(self, id, label=ICON_RESTART)
        self.restartButton.SetToolTip(wx.ToolTip('Restart'))
        self.Bind(wx.EVT_BUTTON, self.OnRestart, self.restartButton)

        self.timeRadio = wx.RadioButton(self, -1, "时钟", style=wx.RB_GROUP)
        self.Bind(wx.EVT_RADIOBUTTON, self.OnRadio, self.timeRadio)
        self.timerRadio = wx.RadioButton(self, -1, "正计时")
        self.Bind(wx.EVT_RADIOBUTTON, self.OnRadio, self.timerRadio)
        self.timer_rRadio = wx.RadioButton(self, -1, "倒计时")
        self.Bind(wx.EVT_RADIOBUTTON, self.OnRadio, self.timer_rRadio)

        # sizer
        sizer = wx.GridBagSizer(hgap=10, vgap=10)
        sizer.Add(self.led, pos=(0, 0), span=(1, 3), flag=wx.EXPAND)

        sizer.Add(self.startButton, pos=(1, 0), flag=wx.EXPAND)
        sizer.Add(self.suspendButton, pos=(1, 1), flag=wx.EXPAND)
        sizer.Add(self.restartButton, pos=(1, 2), flag=wx.EXPAND)

        sizer.Add(self.timeRadio, pos=(2, 0), flag=wx.ALIGN_CENTER)
        sizer.Add(self.timerRadio, pos=(2, 1), flag=wx.ALIGN_CENTER)
        sizer.Add(self.timer_rRadio, pos=(2, 2), flag=wx.ALIGN_CENTER)
        self.SetSizer(sizer)
        self.Fit()

        self.IsSuspend = False

    def OnTimer(self, evt):  # 显示时间事件处理函数
        st = "00 00 00"
        if self.timeRadio.GetValue():  # 显示时间
            st = time.strftime('%H %M %S', time.localtime())
        elif self.timerRadio.GetValue():  # 正向计时
            self.timeToCount += 1
            second = self.timeToCount
            h = second / 3600
            m = second / 60
            s = second % 60
            st = "%02d %02d %02d" % (h, m, s)
        else:  # 逆向计时
            self.timeToCount -= 1
            second = self.timeToCount
            if second <= 0:
                self.timer.Stop()
                dlg = wx.MessageDialog(None, "休息5分钟!".decode('UTF-8'), "Message", wx.OK | wx.ICON_INFORMATION)
                retCode = dlg.ShowModal()
            h = second / 3600
            m = second / 60
            s = second % 60
            st = "%02d %02d %02d" % (h, m, s)
        self.led.SetValue(st)

    def OnPaint(self, evt):
        st = "%02d %02d %02d" % (0, 0, 0)
        self.led.SetValue(st)
        self.Fit()

    def OnStart(self, evt):
        if self.timeRadio.GetValue():  # 显示时间
            self.startButton.Disable()
            self.suspendButton.Disable()
            self.restartButton.Disable()
        elif self.timerRadio.GetValue():  # 正向计时
            if self.IsSuspend:
                self.suspendButton.Enable()
            else:
                self.timeToCount = 0
            self.startButton.Disable()
            self.restartButton.Enable()
            self.suspendButton.Enable()
        else:  # 逆向计时
            if self.IsSuspend:
                self.suspendButton.Enable()
            else:
                self.timeToCount = TIMETOCOUNT
            self.restartButton.Enable()
            self.suspendButton.Enable()
        self.timer.Start(1000)
        self.IsSuspend = False

    def OnStop(self, evt):  # suspend
        if not self.IsSuspend:
            self.startButton.Enable()
            self.suspendButton.Disable()
            self.timer.Stop()
            self.IsSuspend = True

    def OnRestart(self, evt):
        if self.timerRadio.GetValue():  # 正向计时
            if self.IsSuspend:
                self.suspendButton.Enable()
            else:
                self.timeToCount = 0
            self.startButton.Disable()
            self.restartButton.Enable()
            self.suspendButton.Enable()
        else:  # 逆向计时
            self.startButton.Disable()
            self.suspendButton.Enable()
            self.timeToCount = TIMETOCOUNT
        self.timer.Start(1000)
        self.IsSuspend = False

    def OnRadio(self, evt):
        self.timer.Stop()
        self.led.SetValue("00 00 00")
        self.startButton.Enable()
        self.suspendButton.Disable()
        self.restartButton.Disable()
        self.IsSuspend = False


class ClockFrame(wx.Frame):

    def __init__(self, parent=None, id=-1):
        wx.Frame.__init__(self, parent, id, "LED v0.5", size=(300, 170))
        self.SetMaxSize((300, 170))
        self.SetMinSize((300, 170))
        clockWindow = ClockWindow(self, id)


if __name__ == '__main__':
    app = wx.PySimpleApp()
    frame = ClockFrame()
    frame.Show()
    app.MainLoop()