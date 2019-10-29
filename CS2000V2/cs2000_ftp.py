import os
from ftplib import FTP, error_perm


class FTPSync(object):

    def __init__(self):
        self.conn = FTP()
        # self.conn.connect(host, port)

    # 登陆
    def login(self, host, user, passwd):
        if self.conn.connect(host,timeout=5):
            self.conn.login(user, passwd)
        else:
            pass
        return True

    # 友好的关闭连接
    def quit(self):
        try:
            self.conn.quit()
            print('colose ftp connection successfully')
        except Exception as e:
            print('%s' % e)

    # 文件上传实现
    def up_file(self, local_file, ftp_path='.'):
        ftp_path_name = os.path.split(local_file)[1]
        ftp_path = ftp_path + '/' + ftp_path_name
        try:  # 如果文件不存在，调用file.size(filename)会报错
            if self.conn.size(ftp_path) != None:
                print("文件%s已存在" % ftp_path)
                return
        except Exception as e:
            pass
        with open(local_file, 'rb') as file_handler:
            self.conn.storbinary('STOR %s' % ftp_path, file_handler)
            print('文件：%s 已经上传到ftp' % local_file)

    # 文件下载实现
    def down_file(self, local_path, ftp_path):
        if not os.path.isdir(local_path):
            print('请选择文件保存目录路径')
            return
        last_file_name = os.path.split(ftp_path)[1]
        local_file_path = os.path.join(local_path, last_file_name)
        if os.path.isfile(local_file_path):
            local_file_path = local_file_path.replace('\\', '/')
            print('文件:%s 已存在' % local_file_path)
            return
        with open(local_file_path, 'wb') as file_handle:
            self.conn.retrbinary('RETR %s' % ftp_path, file_handle.write)


def ping_ip(ip):
    # linux系统下 实现pingIP地址的功能，-c1指发送报文一次，-w1指等待1
    # backinfo = os.system('ping -c 1 -w 1 %s'%ip)
    # windows系统下 实现pingIP地址的功能，-n 1 指发送报文一次，-w1指等待1
    backinfo = os.system('ping -n 1 -w 1 %s'%ip)
    if backinfo:
        print(backinfo)
        return False
    else:
        print(backinfo)
        return True


if __name__ == '__main__':
    ftp = FTPSync('192.168.2.178')
    ftp.login('root', 'root')
    ftp.up_file(os.path.join(os.getcwd(), '133.txt'))
    # ftp.up_file(os.path.join(os.getcwd(),'root_conf.tar.gz'))
    # ftp.down_file(os.path.join(os.getcwd()), './tools.tar.gz')
    ftp.quit()