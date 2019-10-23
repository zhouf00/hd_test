import os
from ftplib import FTP, error_perm


class FTPSync(object):

    def __init__(self, host, port=21):
        self.conn = FTP()
        self.conn.connect(host, port)

    def login(self, user, passwd):
        self.conn.login(user, passwd)
        print(self.conn.welcome)

    # 友好的关闭连接
    def quit(self):
        try:
            self.conn.quit()
            print('colose ftp connection successfully')
        except Exception as e:
            print('%s' % e)

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

    def down_file(self, local_path, remote_file_path):
        if not os.path.isdir(local_path):
            print('请选择文件保存目录路径')
            return
        last_file_name = os.path.split(remote_file_path)[1]
        local_file_path = os.path.join(local_path, last_file_name)
        if os.path.isfile(local_file_path):
            local_file_path = local_file_path.replace('\\', '/')
            print('文件:%s 已存在' % local_file_path)
            return
        with open(local_file_path, 'wb') as file_handle:
            self.conn.retrbinary('RETR %s' % remote_file_path, file_handle.write)

if __name__ == '__main__':
    ftp = FTPSync('10.100.93.2')
    ftp.login('root', 'root')
    ftp.up_file(os.path.join(os.getcwd(),'root_conf.tar.gz'))
    # ftp.down_file(os.path.join(os.getcwd()), './tools.tar.gz')
    ftp.quit()