#coding : UTF-8
import surroundings
import requests
import time
import csv
import random
import time
import socket
import http.client
from bs4 import BeautifulSoup
from intomysql import MysqlHelp
import xpinyin
# get 
# 解析
# 保存
def get_html(url):                          #解析
    timeout = random.choice(range(50,100))
    while True:
        try:
            rep = requests.get(url,timeout = timeout)
            rep.encoding = 'utf-8'
            break
        except socket.timeout as e:
            print( '3:', e)
            time.sleep(random.choice(range(8,15)))
        except socket.error as e:
            print( '4:', e)
            time.sleep(random.choice(range(20, 60)))
        except http.client.BadStatusLine as e:
            print( '5:', e)
            time.sleep(random.choice(range(30, 80)))
        except http.client.IncompleteRead as e:
            print( '6:', e)
            time.sleep(random.choice(range(5, 15)))
    return rep.text

def get_date(html_text):  #查找要的内容
    bs = BeautifulSoup(html_text, "html.parser")  # 创建BeautifulSoup对象
    body = bs.body                      # 获取body部分
    data = body.find('div', {'class': 'sojob-result'})  # 找到id为7d的div
    ul = data.find('ul')                # 获取ul部分
    li = ul.find_all('li')              # 获取所有的li
    all_info = []                          # 存放所有公司信息的列表
    for day in li:                      # 对每个li标签中的内容进行遍历
        one_info = []                   # 存放一个公司的信息
        zhiwei =day.find('a')           # 找到职位
        if zhiwei is None:              # 判断是否发布职位
            zhiwei = "不详"
        else:
            zhiwei = zhiwei.string
        date = day.find_all('p')            # 找到p标签
        if not date:                        # 判断是否有 p标签
           continue
        dy = date[0].find('span').string    # 待遇
        dd = date[0].find('span',{"class":"area"})             # 地点
        if not dd:                          # 判断是否有地点
            dd = "地点不详"  
        else:
            dd = dd.string
        xl = date[0].find('span',{'class':"edu"}).string  # 学历
        jy = date[0].find_all('span')[3].string           # 经验
        sj = date[1].find('time').string                  #  发布时间
        gs = date[2].find('a').string                     # 公司名称
        if len(date)<=4:                                  # 判断有没有福利项
            fl = "福利不详"
        else:
            fl = date[4].find_all('span')                 #福利
            if len(fl) == 0:
                fl = "福利不详"
            else:
                l3 = []
                for ch in fl:
                    ch = ch.string
                    l3.append(ch)
                    fl = ','.join(l3)
        info  = [zhiwei,sj,gs,dy,dd,jy,xl,fl]
        for ch in info:
            one_info.append(ch)                       #一个人公司的信息
        if one_info not in all_info:
            all_info.append(one_info)                 # 所有公司的信息
    return all_info

def fwrite(data):                               #写入本地
    with open('zhaopin2.csv', 'a',
             errors='ignore', newline='') as f:
            f_csv = csv.writer(f)
            f_csv.writerows(data)

def tomysql(resul):                             #写进数据库 
    mysql = MysqlHelp("db5")
    for ch in resul:
        sql_insert = "insert into zhaopin values\
        (%s,%s,%s,%s,%s,%s,%s,%s);"
        mysql.workOn(sql_insert,ch)

def cpinyin(city,zw,a):  #装换为拼音
    if a == 0:
        pin = xpinyin.Pinyin()
        city = pin.get_pinyin(city,"")
        zw = pin.get_pinyin(zw,"")
        return (city,zw)
    if a == 1:
        s = ''
        pin = xpinyin.Pinyin()
        for ch in city:
            p = pin.get_pinyin(ch,"")[0]
            s += p
        zw = pin.get_pinyin(zw,"")
        return (s,zw)

def get_flush():
    mysql = MysqlHelp("db5")
    sql_insert = "delete from zhaopin;"
    mysql.workOn(sql_insert)


def myurl(c,z,n,a=0):                     # 获取要爬取的网页地址
    # get_flush()                     # 清空服务器
    city,zw = cpinyin(c,z,a)            # 获取城市,职位
    # n = int(input("请输入要显示页数>: "))
    i = 1
    while True:
        url = 'https://www.liepin.com/{}/zp{}' .format(city,zw)
        if i > 1:
            url = url+"/pn{}" .format(i-1)
        html = get_html(url)    
        try: 
            l = get_date(html)
            if not l:                   # 第二次没有内容,结束
                break
        except AttributeError:          # 第二次爬取错误 执行以下
            if 'pn' in url:             # 判断第几次出错
                print("数据加载完毕")
                break
            else:
               myurl(c,z,n,1)                 #第一次读取错误 ,返回重新加载
               return
        fwrite(l)                       #写入本地文件
        # tomysql(l)                      #写进数据库
        if i == n:
            break
        i += 1
    print('完成')


if __name__ == "__main__":              #测试程序的运行
    myurl(city,zw,n)

