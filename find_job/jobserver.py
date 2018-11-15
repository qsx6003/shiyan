#coding : UTF-8

from Zp import *
from socket import * 

# 创建数据报套接字
sockfd = socket(AF_INET,SOCK_DGRAM)

#绑定地址
server_addr = ('0.0.0.0',8888)
sockfd.bind(server_addr)

data,addr = sockfd.recvfrom(1024)
data = (data.decode().split(" "))
print("Reveive from %s:%s"%(addr,data))
myurl(date[0],date[1],1)
sockfd.sendto(b"Thanks for your msg",addr)
    
#关闭套接字
sockfd.close()
