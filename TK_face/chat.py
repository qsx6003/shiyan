#coding=utf8
import requests
import itchat
from itchat.content import * 
import time
# import P_face
from tkinter import *
from tkinter import filedialog
from face_id import *
import threading

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

def run():
    o = threading.Thread(target=unn)
    o.daemon= True
    o.start()
def unn():
    itchat.auto_login(hotReload = True)
    itchat.run()
    # while 1:
    #     time.sleep(0.01)

    #     print("坎坎坷坷扩扩扩扩扩扩")
    #     t.update()




def window():
    global t
    t = Tk()
    t.attributes("-alpha",0.9)
    # t.attributes("-transparentcolor","red")
    t.title("颜值检测")
    t.geometry("400x300")
    t.resizable(False,False)
    # Label(t,compound=CENTER).pack() 
    s = Text(t,height=2,width=80,fg="red",bg="teal")  #输入框属性   字的颜色  背景颜色
    s.place(relx=0,rely=0)   #显示的位置

    print(type(s))
    Button(t,text="打开",font=("楷体",10),command=lambda:filepath(s,t),bg="green")\
            .place(relx=0.88,rely=0.00)  #执行按钮
    global e
    e = Text(t,height=12,width=80,fg="red",bg="teal")
    e.place(relx=0,rely=0.15)# 消息查看窗口
    global g
    print(e)
    g = Text(t,height=5,width=80,fg="red",bg="teal")
    g.place(relx=0,rely=0.6)  #回复消息窗口
    print(g)

    Button(t,text="聊天",font=("楷体",10),command=lambda:run(),bg="green")\
            .place(relx=0.88,rely=0.50) 
             #执行按钮
    
    t.mainloop()




    while 1:
        time.sleep(0.01)
        t.update()

    
    
def filepath(s,t):
    s.delete(0.0,END)
    file_path = filedialog.askopenfilename()
    s.insert(INSERT,file_path)  # 写入地址
    fname = s.get(1.0,END).strip() #得到地址
    t.update()    
    print(fname)
    access_api(fname)


@itchat.msg_register([TEXT,PICTURE],isGroupChat=False)
def tuling_reply(msg):
    if msg['MsgType'] == 1:
        info = msg['User']['NickName']+": "+msg['Text']+'\n'
        print("收到:",msg['Text'])

        print(e)
        e.insert(INSERT,info)
        e.see(END)  # 写入地址
        if msg['User']['NickName']=="独占" or\
            msg['User']['NickName']=="长高。":

            
            itchat.send("working,看到后稍后回复你",msg['FromUserName'])
        elif msg['User']['NickName']=="郭萌":
            pass
        else:
    
            defaultReply = 'I received: ' + msg['Text']
            reply = get_response(msg['Text'])
            time.sleep(1)
            print('回复:',reply)
                # a or b的意思是，如果a有内容，那么返回a，否则返回b
                # 有内容一般就是指非空或者非None，你可以用`if a: print('True')`来测试
            e.insert(INSERT,"回复 :"+reply+"\n")
            t.update()  # 写入地址
            return reply or defaultReply
    else:
        msg["Text"](msg['FileName'])
        P_face.main(msg['FileName'])
        # itchat.send('@%s@%s'%('img' if msg['Type'] == 'Picture' else 'fil', msg['FileName']), msg['FromUserName'])
        itchat.send("@img@%s"%msg['FileName'],msg['FromUserName'])
        return "准否?"
# 为了让实验过程更加方便（修改程序不用多次扫码），我们使用热启动

# h = threading.Thread(target=window)
# h.start()
window()
