"""
ftp_server.py
    文件服务器

    【1】 分为服务端和客户端，要求可以有多个客户端同时操作。
    ftp_server      ftp_client
    【2】 客户端可以查看服务器文件库中有什么文件。

    【3】 客户端可以从文件库中下载文件到本地。
     down
    【4】 客户端可以上传一个本地文件到文件库。
     up
    【5】 使用print在客户端打印命令输入提示，引导操作

    1.技术点确定
     *并发模型  ： 多线程
     *数据传输  ：  tcp传输
    2.结构设计
      *  类封装  将基本文件操作功能为类
    3.功能模块
        * 搭建网络通信模型
        * 查看文件列表
        * 下载文件
        * 上传文件
    4.协议确定

      L  请求文件列表
      Q  退出
      G  下载文件
      P  上传文件

"""
from threading import Thread
import signal
import os
from time import sleep
from time import strftime

from socket import *



class FTPServer(Thread):
    def __init__(self,connfd,addr):
        self.connfd = connfd
        self.addr = addr
        super().__init__()
    #查看文件列表
    def get_file_list(self):
        print('get list')
        #获取文件列表
        file_list = os.listdir(FILE_LIBRARY_PATH)
        if not file_list:
            self.connfd.send('文件库为空')
            return
        else:
            self.connfd.send(b'OK')
            sleep(0.1) #防止 粘包
        filelist = ''
        for i in file_list:
                #不是隐藏文件
            if i[0] != '.' and os.path.isfile(FILE_LIBRARY_PATH+i):
                filelist += i+'\n'
        self.connfd.send(filelist.encode())


    #下载文件
    def get_down(self,file_name):
        try:
            f = open(FILE_LIBRARY_PATH+file_name,'rb')
        except Exception:
            #打开文件失败
            self.connfd.send('文件不存在'.encode())
            return
        else:
            self.connfd.send(b"OK")
            sleep(0.1)
        #发送文件
        while True:
            data = f.read(1024)
            if not data:
                sleep(0.1)
                self.connfd.send(b'Over')
                return #结束函数
            self.connfd.send(data)
        f.close()

    #上传文件
    def put_up(self,file_name):
        # 获取文件列表
        file_list = os.listdir(FILE_LIBRARY_PATH)
        if file_name in file_list:
            self.connfd.send('文件已存在'.encode())
            return
        self.connfd.send(b'OK')
        sleep(0.1)
        f = open(FILE_LIBRARY_PATH+file_name,'wb')
        while True:
            up_data = self.connfd.recv(1024)
            print(up_data)
            if up_data == b'Over':
                print('完成')
                break
            f.write(up_data)
        f.close()

    #处理操作
    def run(self):
        print('开始通信')
        while True:
            data = self.connfd.recv(1024).decode()
            print(data)
            if not data or data == "Q":
                print(self.addr,'退出')
                return #线程结束
            elif data.strip() == 'L':
                self.get_file_list()
            elif data[0] == "G":
                file_name = data.split(' ')[-1]
                self.get_down(file_name)
            elif data[0] == "P":
                file_name = data.split(' ')[-1]
                self.put_up(file_name)
        self.connfd.close()


# 搭建网络服务端模型
signal.signal(signal.SIGCHLD,signal.SIG_IGN)
#全局变量
FILE_LIBRARY_PATH = '/home/tarena/1905/mouth02/concur/ftp_server/ftp_file_library/'
SERVER_ADDR = ('127.0.0.1',8080)
def main():
    sockfd = socket(AF_INET,SOCK_STREAM)
    sockfd.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    sockfd.bind(SERVER_ADDR)
    sockfd.listen(6)

    print('SUCCESS ftp_server waiting。。。')
    while True:
        try:
            conn,addr = sockfd.accept()
            print("connect from ",addr)
        except KeyboardInterrupt:
            os._exit(0)
        except Exception as e:
            print(e)
            continue

        #创建多线程连接
        ft = FTPServer(conn,addr)
        ft.setDaemon(True)
        ft.start()


if __name__ == '__main__':
    main()
