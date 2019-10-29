import sys, time,datetime
import cgitb
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget,QTextBrowser,
                             QHBoxLayout, QVBoxLayout, QLabel, QComboBox, QPushButton,
                             QDateEdit, QSpacerItem, QFrame, QSizePolicy, QSplitter,
                             QRadioButton, QGroupBox, QCheckBox, QLineEdit, QAction,
                             QTextEdit, QFileDialog, QMessageBox, QFormLayout)
from PyQt5.QtCore import Qt, QTimer, QRect, QCoreApplication
from cs2000V2_main import FTPSync, SerialClient, TelnetClient, port_list, ResetHost, TelnetInstall


versions = ['v1', 'v2']

# class Ui_Frame(QMainWindow):
#
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.setupUi(self)

class Ui_Frame(object):

    def setupUi(self, MainWindow):
        MainWindow.setObjectName('MainWindow')
        # 设置窗口大小并固定大小
        MainWindow.resize(780, 460)
        MainWindow.setFixedSize(780, 460)

        # 串口内容
        self.ser_groupbox = QGroupBox(MainWindow)
        self.ser_groupbox.setGeometry(QRect(20 ,20, 190, 140))
        self.ser_grouplayout = QFormLayout(self.ser_groupbox)
        self.ser_grouplayout.setContentsMargins(10, 10, 10, 10)
        self.ser_grouplayout.setSpacing(10)

        self.port_lb = QLabel(self.ser_groupbox)
        self.port_combox = QComboBox(self.ser_groupbox)
        self.ser_grouplayout.setWidget(0, QFormLayout.LabelRole, self.port_lb)
        self.ser_grouplayout.setWidget(0, QFormLayout.FieldRole, self.port_combox)
        self.baud_lb = QLabel(self.ser_groupbox)
        self.baud_combox = QComboBox(self.ser_groupbox)
        self.ser_grouplayout.setWidget(1, QFormLayout.LabelRole, self.baud_lb)
        self.ser_grouplayout.setWidget(1, QFormLayout.FieldRole, self.baud_combox)
        self.open_button = QPushButton(self.ser_groupbox)
        self.ser_grouplayout.setWidget(2, QFormLayout.SpanningRole, self.open_button)

        # telnet内容
        self.tel_GroupBox = QGroupBox(MainWindow)
        self.tel_GroupBox.setGeometry(QRect(20, 170, 190, 200))
        self.tel_GroupLayout = QFormLayout(self.tel_GroupBox)
        self.tel_GroupLayout.setContentsMargins(5, 10, 5, 5)
        self.tel_GroupLayout.setSpacing(10)

        self.dgmid_lb = QLabel(self.tel_GroupBox)
        self.dgmid_line = QLineEdit(self.tel_GroupBox)
        self.tel_GroupLayout.setWidget(0, QFormLayout.LabelRole, self.dgmid_lb)
        self.tel_GroupLayout.setWidget(0, QFormLayout.FieldRole, self.dgmid_line)
        self.ip_lb = QLabel(self.tel_GroupBox)
        self.ip_line = QLineEdit(self.tel_GroupBox)
        self.tel_GroupLayout.setWidget(1, QFormLayout.LabelRole, self.ip_lb)
        self.tel_GroupLayout.setWidget(1, QFormLayout.FieldRole, self.ip_line)
        self.serverip_lb = QLabel(self.tel_GroupBox)
        self.serverip_line = QLineEdit(self.tel_GroupBox)
        self.tel_GroupLayout.setWidget(2, QFormLayout.LabelRole, self.serverip_lb)
        self.tel_GroupLayout.setWidget(2, QFormLayout.FieldRole, self.serverip_line)
        self.serverport_lb = QLabel(self.tel_GroupBox)
        self.serverport_line = QLineEdit(self.tel_GroupBox)
        self.tel_GroupLayout.setWidget(3, QFormLayout.LabelRole, self.serverport_lb)
        self.tel_GroupLayout.setWidget(3, QFormLayout.FieldRole, self.serverport_line)


        # 接受区
        self.vericalGroupBox = QGroupBox(MainWindow)
        self.vericalGroupBox.setGeometry(QRect(220, 20, 440, 280))
        vericalGroupLayout = QFormLayout(self.vericalGroupBox)
        vericalGroupLayout.setContentsMargins(10, 10, 10, 10)
        self.receive_text = QTextBrowser(self.vericalGroupBox)
        vericalGroupLayout.addWidget(self.receive_text)

        # 检查内容
        self.exa_reset = QCheckBox(MainWindow)
        self.exa_changeip = QCheckBox(MainWindow)
        self.exa_upfile = QCheckBox(MainWindow)
        self.exa_install = QCheckBox(MainWindow)
        self.exa_system = QCheckBox(MainWindow)
        self.exa_showid = QCheckBox(MainWindow)
        self.exa_serverip = QCheckBox(MainWindow)
        self.exa_serverport = QCheckBox(MainWindow)
        self.exa_button = QPushButton(MainWindow)
        self.exa_re_button = QPushButton(MainWindow)

        self.exa_reset.setGeometry(QRect(670, 30, 100, 20))
        self.exa_changeip.setGeometry(QRect(670, 60, 100, 20))
        self.exa_upfile.setGeometry(QRect(670, 90, 100, 20))
        self.exa_install.setGeometry(QRect(670, 120, 100, 20))
        self.exa_system.setGeometry(QRect(670, 150, 100, 20))
        self.exa_showid.setGeometry(QRect(670, 180, 100, 20))
        self.exa_serverip.setGeometry(QRect(670, 210, 100, 20))
        self.exa_serverport.setGeometry(QRect(670, 240, 100, 20))
        self.exa_button.setGeometry(QRect(670, 270, 90, 30))
        self.exa_re_button.setGeometry(QRect(670, 310, 90, 30))

        # 发送区
        self.vericalGroupBox_2 = QGroupBox(MainWindow)
        self.vericalGroupBox_2.setGeometry(220, 305, 440, 65)
        vericalGroupLayout_2 = QFormLayout(self.vericalGroupBox_2)
        vericalGroupLayout_2.setContentsMargins(10, 10, 10, 10)
        self.send_text = QTextEdit(self.vericalGroupBox_2)
        vericalGroupLayout_2.addWidget(self.send_text)
        self.send_button = QPushButton(MainWindow)
        self.send_button.setGeometry(QRect(540, 385, 125, 65))

        # dgmid
        # self.setGroupBox = QGroupBox(MainWindow)
        # self.setGroupBox.setGeometry(20, 380, 190, 70)
        # self.setGroupLayout = QFormLayout(self.setGroupBox)
        # self.setGroupLayout.setContentsMargins(10, 10, 10, 10)
        # self.dgmid_line = QLineEdit(self.setGroupBox)
        # self.setGroupLayout.setWidget(1, QFormLayout.SpanningRole, self.dgmid_line)

        # 上传文件路径
        self.fileGroupBox = QGroupBox(MainWindow)
        self.fileGroupBox.setGeometry(220, 380, 300, 70)
        self.fileGroupLayout = QFormLayout(self.fileGroupBox)
        self.fileGroupLayout.setContentsMargins(10, 10, 10, 10)
        self.file_line = QLineEdit(MainWindow)
        self.file_button = QPushButton(MainWindow)
        self.fileGroupLayout.setWidget(1, QFormLayout.LabelRole, self.file_button)
        self.fileGroupLayout.setWidget(1, QFormLayout.SpanningRole, self.file_line)

        self.retranslateUi(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QCoreApplication.translate
        MainWindow.setWindowTitle(_translate('MainWindow', 'MainWindow'))
        self.ser_groupbox.setTitle(_translate('MainWindow', '串口设置'))
        self.port_lb.setText(_translate('MainWindow', '串口选择：'))
        self.baud_lb.setText(_translate('MainWindow', '波特率：'))
        self.baud_combox.addItem(_translate('MainWindow', '115200'))
        self.open_button.setText(_translate('MainWindow', '打开串口'))
        # self.close_button.setText(_translate('MainWindow', '关闭串口'))

        self.tel_GroupBox.setTitle(_translate('MainWindow', '网络设置'))
        self.ip_lb.setText(_translate('MainWindow', '设备IP'))
        self.ip_line.setPlaceholderText(_translate('MainWindow', 'ip地址为'))
        self.dgmid_lb.setText(_translate('MainWindow', 'dgmID'))
        self.dgmid_line.setPlaceholderText(_translate('MainWindow', '请输入8位dgmid'))
        self.serverip_lb.setText(_translate('MainWindow', '服务器IP'))
        self.serverip_line.setText(_translate('MainWindow', '192.168.2.89'))
        # self.serverip_line.setPlaceholderText(_translate('MainWindow', '服务器IP'))
        self.serverport_lb.setText(_translate('MainWindow', '服务器端口'))
        self.serverport_line.setText(_translate('MainWindow', '80'))
        # self.serverport_line.setPlaceholderText(_translate('MainWindow', '端口'))
        # self.connect_button.setText(_translate('MainWindow', '连接'))

        self.exa_reset.setText(_translate('MainWindow', '烧写核心板'))
        self.exa_changeip.setText(_translate('MainWindow', '重启修改IP'))
        self.exa_upfile.setText(_translate('MainWindow', '上传升级包'))
        self.exa_install.setText(_translate('MainWindow', '安装升级包'))
        self.exa_system.setText(_translate('MainWindow', '检查状态完毕'))
        self.exa_showid.setText(_translate('MainWindow', 'showid'))
        self.exa_serverip.setText(_translate('MainWindow', 'serverip'))
        self.exa_serverport.setText(_translate('MainWindow', 'serverport'))
        self.exa_button.setText(_translate('MainWindow', '自动测试'))
        self.exa_re_button.setText(_translate('MainWindow', '重置'))

        self.vericalGroupBox.setTitle(_translate('MainWindow', '接收区'))
        self.vericalGroupBox_2.setTitle(_translate('MainWindow', '发送区'))
        self.send_button.setText(_translate('MainWindow', '发送'))

        # self.setGroupBox.setTitle(_translate('MainWindow', 'dgmid:（第一步）'))

        self.fileGroupBox.setTitle(_translate('MainWindow', '文件上传'))
        self.file_button.setText(_translate('MainWindow', '上传'))



if __name__ == '__main__':
    cgitb.enable(format="text")
    app = QApplication(sys.argv)
    win = Ui_Frame()
    win.show()
    sys.exit(app.exec_())