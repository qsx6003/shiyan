#coding=utf8
import requests
import itchat
from itchat.content import * 
import time

KEY = 'f4680211d53c427bba483137c73926ad'

def get_response(msg):
    apiUrl = 'http://www.tuling123.com/openapi/api'
    data = {
        'key'    : KEY,
        'info'   : msg,
        'userid' : '空空',
    }
    try:
        r = requests.post(apiUrl, data=data).json()
        return r.get('text')
    except:
        return

@itchat.msg_register([TEXT,PICTURE],isGroupChat=False)
def tuling_reply(msg):
    if msg['MsgType'] == 1:
        print("收到:",msg['Text'])
        defaultReply = 'I received: ' + msg['Text']
        reply = get_response(msg['Text'])
        time.sleep(2)
        print('回复:',reply)
            # a or b的意思是，如果a有内容，那么返回a，否则返回b
            # 有内容一般就是指非空或者非None，你可以用`if a: print('True')`来测试
        return "智能回复: "+reply or defaultReply
    else:
        msg["Text"](msg['FileName'])
        # itchat.send('@%s@%s'%('img' if msg['Type'] == 'Picture' else 'fil', msg['FileName']), msg['FromUserName'])
        itchat.send("@img@181109-103610.png",msg['FromUserName'])
        return "全国最帅的男人"
# 为了让实验过程更加方便（修改程序不用多次扫码），我们使用热启动
itchat.auto_login(hotReload = True)
itchat.run()
