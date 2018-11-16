#coding : UTF-8

from Zp import *
from socket import * 

ADDR = ("0.0.0.0",8899)

def job_sever(ADDR):
# 创建数据报套接字
    sockfd = socket(AF_INET,SOCK_DGRAM)


    #绑定地址
    server_addr = (ADDR)
    sockfd.bind(server_addr)
    while True:
        data,addr = sockfd.recvfrom(1024)
        data = (data.decode().split(" "))
        print("Reveive from %s:%s"%(addr,data))
        myurl(date[0],date[1],1)
        sockfd.sendto(b"Thanks for your msg",addr)   
    #关闭套接字
    sockfd.close()
if __name__== "__main__":
    job_sever(ADDR)

