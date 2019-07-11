"""
chat romm
env: python3.6
socket udp & fork
    通信协议设置
    * 进入聊天室：L
    * 聊天 ： C
    * 退出 ： Q
    * 服务器反馈： OK 成功 其他表示失败
"""

from socket import *
import os,sys
import time
"""全局变量：很多封装模块都要用的"""
#服务器地址
ADDR = ("0.0.0.0",7890)
#聊天室成员列表
user = {}
#登录处理
def do_login(s, name, address):
    if name in user:
        s.sendto('用户名存在'.encode(), addr)
        return
    s.sendto(b'OK', address)
    # 通知其他人
    msg = '欢迎“%s”进入聊天室' % name
    for i in user:
        s.sendto(msg.encode(), user[i])
    user[name] = address
#消息处理
def msg_mode(s,name,data):
    text = time.strftime('%H:%M:%S')+'  '+name+':'+data
    for i in user:
        if i != name:
            s.sendto(text.encode(),user[i])
#退出
def do_quit(s,name):
    for i in user:
        if name != i:
            msg = '%s 退出聊天室'%name
            s.sendto(msg.encode(),user[i])
        else:
            s.sendto(b'Exit',user[i])
    del user[name]
#处理请求
def do_request(s):
    while True:
        data,addr = s.recvfrom(1024)
        tmp = data.decode().split(' ')
        if tmp[0] == "L":
            do_login(s,tmp[1],addr)
        elif tmp[0] == "C":
            text = ' '.join(tmp[2:])
            msg_mode(s,tmp[1],text,)
        elif tmp[0] == 'Q':
            do_quit(s,tmp[1])

def main():
    sockfd = socket(AF_INET,SOCK_DGRAM)
    sockfd.bind(ADDR)
    #打印服务器
    print("||--------------聊天室---------------||")
    pid = os.fork()
    if pid == 0:
        while True:
            msg = input('管理员消息')
            msg = 'C 管理员 '+msg
            sockfd.sendto(msg.encode(),ADDR)
    elif pid >0:
        # 请求处理函数
        do_request(sockfd)
main()