#!/usr/bin/python
# coding: utf-8
import itchat
import os
import pandas as pd
import matplotlib.pyplot as plot
from wordcloud import WordCloud
from pyecharts import Bar, Page
import jieba
import sys
import itchat
import csv

# 获取所有的群聊列表
def getRoomList():
    roomslist = itchat.get_chatrooms()
    return roomslist.text
#获取指定群聊的信息
def getRoomMsg(roomName):
    itchat.dump_login_status()
    myroom = itchat.search_chatrooms(name=roomName)
    return myroom
def fwrite(data):   #写入本地
    with open('Qun_info.csv', 'a', errors='ignore', newline='') as f:
            f_csv = csv.writer(f)
            f_csv.writerows(data)


def main():
    l = []
    l2 = []
    itchat.auto_login(hotReload=True)    #自动登陆
    l=getRoomList()
    print("-----------------------------------------------")
    myroom=(l[2]['NickName'])
    roomMsg = getRoomMsg(myroom)
    print(roomMsg[0])

    print("---------------------------------------------------------")
    gsq = itchat.update_chatroom(roomMsg[0]['UserName'], detailedMember=True)

    # for ch in gsq['MemberList']:
    #     l=[ch['NickName'].replace(" ",""),ch['Sex'],ch['Signature'].replace(" ","").replace("\n",""),ch['City'],ch['DisplayName']]
    #     l2.append(l)
    # fwrite(l2)
if __name__=='__main__':
   main()