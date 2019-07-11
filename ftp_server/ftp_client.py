"""
ftp 文件服务器
"""

from socket import socket
import sys
from time import sleep
#客户端文件处理类
class FTPClient():
    """客户端处理 查看 上传 下载 退出"""
    def __init__(self,sockfd):
        self.sockfd = sockfd
    #获取文件列表
    def do_list(self):
        self.sockfd.send(b'L')
        #等待回复
        data = self.sockfd.recv(128).decode()
        if data == 'OK':
            data = self.sockfd.recv(4096)
            print(data.decode())

        else:
            print(data)
    #退出
    def do_quit(self):
        #请求退出
        self.sockfd.send(b'Q')
        self.sockfd.close()
        sys.exit('客户端退出')
    #下载文件
    def get_down_file(self,file_name):
        #发送请求
        self.sockfd.send(('G '+file_name).encode())
        #等待回复
        data = self.sockfd.recv(128).decode()
        if data == 'OK':
            print('开始下载')
            f = open(file_name,'wb')
            while True:
                down_data = self.sockfd.recv(1024)
                if down_data == b'Over':
                    break
                f.write(down_data)
            f.close()
            print('下载完成')
        else:
            print(data)
    #上传文件
    def put_up_file(self,file_name):
        #发送请求
        self.sockfd.send(('P '+file_name).encode())
        #等待回复
        data = self.sockfd.recv(1024).decode()
        if data == "OK":
            print('开始上传')
            f = open(file_name,'rb')
            while True:
                up_data = f.read(1024)
                if not up_data:
                    sleep(0.2)
                    self.sockfd.send(b'Over')
                    break
                self.sockfd.send(up_data)
            f.close()
            print('上传完成')
        else:
            print(data)

#全局变量
ADDR = ('127.0.0.1',8080)
#链接服务器
menu = """\n
    +===========FTP Server==========+
    |      L:    get list           |
    |      G:    get down file      |
    |      P:    put up file        |
    |      Q:    quit               |
    +===============================+
    """
def main():
    sockfd = socket()
    try:
        sockfd.connect(ADDR)
    except Exception as e:
        print("连接失败，错误【%s】"%e)
        return
    print('登录成功！。。。。。。。。。。。')

    #实例化操作对象
    ftp = FTPClient(sockfd)

    while True:
        print(menu)
        msg = input('>>>>>')
        if msg == 'l' or msg == "L":
            ftp.do_list()
        elif msg == "q" or msg == "Q":
            ftp.do_quit()
        elif msg == 'G' or msg == 'g':
            file_name = input('plase input file name:').strip()
            ftp.get_down_file(file_name)
        elif msg =='p'or msg == "P":
            file_name = input('plase input file name:').strip()
            ftp.put_up_file(file_name)
    sockfd.close()


if __name__ == '__main__':
    main()
