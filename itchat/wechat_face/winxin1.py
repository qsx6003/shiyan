#coding=utf8
import requests
import itchat
from itchat.content import * 
import time
import P_face
KEY = 'd5f09b9ea887400185658545f3e1db39'

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
        print(msg['User']['NickName'])
        if msg['User']['NickName']=="独占" or\
            msg['User']['NickName']=="长高。":

            print("收到:",msg['Text'])
            itchat.send("working,看到后稍后回复你",msg['FromUserName'])
        elif msg['User']['NickName']=="郭萌":
            pass
        else:
            print("收到:",msg['Text'])
            defaultReply = 'I received: ' + msg['Text']
            reply = get_response(msg['Text'])
            time.sleep(2)
            print('回复:',reply)
                # a or b的意思是，如果a有内容，那么返回a，否则返回b
                # 有内容一般就是指非空或者非None，你可以用`if a: print('True')`来测试
            return reply or defaultReply
    else:
        msg["Text"](msg['FileName'])
        P_face.main(msg['FileName'])
        # itchat.send('@%s@%s'%('img' if msg['Type'] == 'Picture' else 'fil', msg['FileName']), msg['FromUserName'])
        itchat.send("@img@%s"%msg['FileName'],msg['FromUserName'])
        return "准否?"
# 为了让实验过程更加方便（修改程序不用多次扫码），我们使用热启动
itchat.auto_login(hotReload = True)
itchat.run()
