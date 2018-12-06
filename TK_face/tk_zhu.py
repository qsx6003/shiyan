from tkinter import *
from tkinter import filedialog
from face_id import *

def window():
    t = Tk()
    t.attributes("-alpha",0.9)
    # t.attributes("-transparentcolor","red")
    t.title("颜值检测")
    t.geometry("400x30")
    t.resizable(False,False)

    Label(t,compound=CENTER).pack() 
    s = Text(t,height=6,width=80,fg="black",bg="teal")  #输入框属性   字的颜色  背景颜色
    s.place(relx=0,rely=0)   #显示的位置
    Button(t,text="打开",font=("楷体",10),command=lambda:filepath(s),bg="green")\
            .place(relx=0.88,rely=0.05)  #执行按钮
    t.mainloop()

def filepath(s):
    s.delete(0.0,END)
    file_path = filedialog.askopenfilename()
    s.insert(INSERT,file_path)  # 写入地址
    fname = s.get(1.0,END).strip() #得到地址
    print(fname)
    access_api(fname)

window()
