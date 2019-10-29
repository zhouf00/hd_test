import serial, cgitb, sys, os
from test_gui import QMainWindow, Ui_Frame, QApplication, QMessageBox, QTimer, QFileDialog
from test_com_1 import port_list
from cs2000_ftp import FTPSync, ping_ip

# loginheader = b'SWA3300-ZJZZ login:'
# header = b'root@SWA3300-ZJZZ:~# '
# qwenter = b'Press qw to cmdline'
# uboot_header = b'Sanway@335x->'


class Qt_Main(Ui_Frame, QMainWindow):

    sw_auto = False
    sw_telnet = False
    sw_install = False
    exa_system_num = 0

    def __init__(self):
        super(Qt_Main, self).__init__()
        self.setupUi(self)
        self.setWindowTitle('测试abc')
        self.init()

        self.ser = serial.Serial()
        self.ftp = FTPSync()
        # self.tn = telnetlib.Telnet()

    def init(self):
        # dgmid按钮
        self.dgmid_line.textChanged.connect(self._show_ip)

        # 上传文件
        self.file_button.clicked.connect(self._open_file)
        self.file_line.textChanged.connect(self._up_file)

        # 串口显示
        self.port_combox.addItems(port_list())
        self.port_combox.setCurrentIndex(1)

        # 打开关闭串口
        self.open_button.clicked.connect(self._port_open)

        # 连接断开telnet
        # self.connect_button.clicked.connect(self._telnet_open)

        # 发送数据
        self.send_button.clicked.connect(self._data_send)

        # 定时发送数据
        self.timer_send = QTimer()
        # self.timer_send.timeout.connect()

        # 定时接收数据 串口
        self.timer = QTimer(self)
        self.timer.timeout.connect(self._data_receive)

        # 定时接收数据 telnet
        # self.timer_telnet = QTimer()
        # self.timer_telnet.timeout.connect(self._data_receive_telnet)

        # 自动测试
        self.exa_changeip.stateChanged.connect(self._upfile_message)
        self.exa_button.clicked.connect(self._start_test)
        self.exa_re_button.clicked.connect(self._test_re)
        self.exa_system.stateChanged.connect(self._export_log)

        # 清除接口窗口

    def _port_open(self):
        self.ser.port = self.port_combox.currentText()
        self.ser.baudrate = int(self.baud_combox.currentText())

        if self.ser.isOpen():
            self.timer.stop()
            self.timer_send.stop()
            try:
                self.ser.close()
            except:
                pass
            else:
                self.open_button.setText('打开串口')
            self.connect_button.setEnabled(True)
            # self.ser_groupbox.setTitle('串口状态（已开启）')
        else:
            try:
                self.ser.open()
            except:
                QMessageBox.critical(self, "Port Error", "此串口不能或端口被占用")
                return None
            else:
                self.open_button.setText('关闭串口')
            self.timer.start(2)
            # self.connect_button.setEnabled(False)

    def _show_ip(self):
        dgmid = self.dgmid_line.text()
        # version = self.h1_combox_versions.currentText()
        if dgmid != '':
            new_ip = '192.168.2.%d' % (100 + int(dgmid) % 100)
            self.ip_line.setText(str(new_ip))
        else:
            self.ip_line.clear()

    def _open_file(self):
        self.file_line.clear()
        filepath = QFileDialog.getOpenFileName(self, '选择文件', '*.tar')
        self.file_line.setText(filepath[0])

    def _upfile_message(self):
        if self.exa_changeip.isChecked():
            QMessageBox.information(self, "", '请上传升级包')
            self._open_file()
        else:
            pass

    def _up_file(self):
        file = self.file_line.text()
        if file:
            ip = self.ip_line.text()
            if ip:
                if ping_ip(ip):
                    pass
                else:
                    QMessageBox.critical(self, "Port Error", '[%s]网络不通，请检查后上传' % ip)
                    self.sw_auto = False
                    return
            else:
                QMessageBox.critical(self, "Port Error", 'IP地址栏为空')
                return
            try:
                self.ftp.login(self.ip_line.text(), 'root', 'root')
                self.ftp.up_file(self.file_line.text())
            except Exception as e:
                self.file_line.clear()
                QMessageBox.critical(self, "Port Error", str(e))
            else:
                self.ftp.quit()

                self.exa_upfile.setChecked(True)
        else:
            self.exa_upfile.setChecked(False)
            pass

    def _telnet_open(self):
        self.receive_text.insertPlainText('网络连接中...')
        self.ip = self.ip_line.text()

        if self.sw_telnet:
            self.tn.close()
            self.sw_telnet = False
            self.connect_button.setText('连接')
        else:
            try:
                self.tn.open(self.ip, timeout=5)
            except:
                self.connect_button.setText('连接')
                QMessageBox.critical(self, "Telnet Error", "网络连接失败...")
                return None
            else:
                self.connect_button.setText('断开连接')
                self.sw_telnet = True

    # 发送数据
    def _data_send(self):
        if self.ser.isOpen():
            input_s = self.send_text.toPlainText()

            if input_s != "":
                input_s = (input_s + '\n').encode()
            print(self.ser.write(input_s))
            print('输入', input_s)
            self.send_text.clear()
        else:
            pass

    # 接收数据
    def _data_receive(self):
        try:
            num = self.ser.inWaiting()
        except:
            self._port_open()
            return None
        if num > 0:
            data = self.ser.read(num)
            self.receive_text.insertPlainText(data.decode())
            print(data)
            if self.sw_auto:
                if not self.exa_changeip.isChecked() or not self.exa_reset.isChecked():
                    print('进入第一步')
                    self._test_reset(data)
                elif not self.exa_install.isChecked() and self.exa_upfile.isChecked():
                    print('进入第二步')
                    self._test_install(data)
                elif not self.exa_showid.isChecked() and self.exa_install.isChecked():
                    self._test_examine(data, self.exa_showid, './showid')
                elif not self.exa_serverip.isChecked() and self.exa_showid.isChecked():
                    self._test_examine(data, self.exa_serverip, './serverip', self.serverip_line.text())
                elif not self.exa_serverport.isChecked() and self.exa_serverip.isChecked():
                    self._test_examine(data, self.exa_serverport, './serverport', self.serverport_line.text())
                elif self.exa_system_num == 3:
                    self.exa_system.setChecked(True)
                    self.sw_auto = False
            else:
                pass
            # 获取光标到text中去
            textCursor = self.receive_text.textCursor()
            textCursor.movePosition(textCursor.End)
            self.receive_text.setTextCursor(textCursor)
        else:
            pass

    # 自动测试按钮
    def _start_test(self):
        self.dgmid = self.dgmid_line.text()
        if not self.dgmid:
            QMessageBox.critical(self, "Telnet Error", "dgmid为空")
            return
        else:
            pass
        if self.ser.isOpen():
            self.sw_auto = True
            self.ser.write('\n'.encode())
        else:
            self._port_open()
            self.sw_auto = True
            self.ser.write('\n'.encode())

    # 重置
    def _test_re(self):
        if self.sw_auto:
            self.sw_auto = False
        else:
            pass
        self.exa_reset.setChecked(False)
        self.exa_changeip.setChecked(False)
        self.exa_upfile.setChecked(False)
        self.exa_install.setChecked(False)
        self.exa_system.setChecked(False)
        self.exa_showid.setChecked(False)
        self.exa_serverip.setChecked(False)
        self.exa_serverport.setChecked(False)

    # 烧写核心板，修改ip
    def _test_reset(self, data):
        if data.find(b'root@SWA3300-ZJZZ:') != -1:
            if not self.exa_reset.isChecked():
                self.ser.write('reboot\n'.encode())
            elif not self.exa_changeip.isChecked() and self.exa_reset.isChecked():
                self.ser.write(('ifconfig eth0 %s\nifconfig eth1 down\n' % self.ip_line.text()).encode())
                self.ser.write('cd /work/data\n'.encode())
                self.exa_changeip.setChecked(True)
        elif data.find(b'login:') != -1:
            self.ser.write('root\n'.encode())
        elif data.find(b'Password:') != -1:
            self.ser.write('root\n'.encode())
        elif data.find(b'Sanway@335x->') != -1:
            if not self.exa_reset.isChecked():
                self.ser.write('\n'.encode())
                self.ser.write('nand erase.chip\n'.encode())
                self.exa_reset.setChecked(True)
            else:
                self.ser.write('reset\n'.encode())
        elif data.find(b'Press qw to cmdline') != -1 and not self.exa_reset.isChecked():
            self.ser.write('qwqwqw'.encode())

    # 安装软件
    def _test_install(self, data):
        if data.find(b'./deploy2.sh: No such file or directory') != -1:
            QMessageBox.critical(self, "Telnet Error", "deploy2.sh文件不存在，请检查路径")
            self.sw_auto = False
            return
        elif data.find(('Changed DGU id %s OK'%self.dgmid).encode()) != -1:
            self.ser.write('cd\n'.encode())
            self.exa_install.setChecked(True)
            return
        elif data.find(b'root@SWA3300-ZJZZ:') != -1:
            if not self.sw_install:
                self.ser.write(('tar zxvf %s\n' % self.file_line.text().split('/')[-1]).encode())
                self.sw_install = True
            else:
                self.ser.write(('./deploy2.sh %s\n' % self.dgmid_line.text()).encode())
        else:
            pass

    # 系统检查
    def _test_examine(self, data, cb, comm, args=''):
        if data.find(b'No such file or directory') != -1:
            QMessageBox.critical(self, "Telnet Error", "文件不存在，请检查路径")
            self.sw_auto = False
            return
        elif data.find(b'root@SWA3300-ZJZZ:') != -1:
                self.ser.write(('%s %s\n'%(comm, args)).encode())
                cb.setChecked(True)
                self.exa_system_num += 1
        else:
            pass

    # 日志保存
    def _export_log(self):
        res = self.receive_text.toPlainText()
        logpath = os.path.join(os.getcwd(),'logs')
        if not os.path.exists(logpath):
            os.mkdir(logpath)
        logfile = os.path.join(logpath, self.dgmid_line.text()+'.log')
        print(logfile)
        fp = open(logfile, 'a+')
        fp.write(res)
        fp.close()

if __name__ == '__main__':
    cgitb.enable(format="text")
    app = QApplication(sys.argv)
    win = Qt_Main()
    win.show()
    sys.exit(app.exec_())