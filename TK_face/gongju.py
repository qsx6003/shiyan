from tkinter import *
import os
def menu():
    root = Tk()
    root.attributes("-alpha",0.9)
    root.title("集合")
    root.geometry('200x200')
    button(root)
    root.mainloop()
def button(root):
    Button(root,text="颜值检测",font=("华文行楷",20),width=6,height=3,command=lambda:filepath(s,t),bg="aqua")\
            .place(relx=0.0,rely=0.00)
    Button(root,text="",font=("华文行楷",20),width=6,height=3,command=lambda:filepath(s,t),bg="aqua")\
            .place(relx=0.5,rely=0.00)
    Button(root,text="打开",font=("华文行楷",20),width=6,height=3,command=lambda:filepath(s,t),bg="aqua")\
            .place(relx=0.0,rely=0.5)
    Button(root,text="打开",font=("华文行楷",20),width=6,height=3,command=lambda:filepath(s,t),bg="aqua")\
            .place(relx=0.5,rely=0.5)
    
    # Button(root,text="打开",font=("楷体",50),command=lambda:filepath(s,t),bg="green")\
    #         .place(relx=0.3,rely=0.00) 
    # Button(root,text="打开",font=("楷体",10),command=lambda:filepath(s,t),bg="green")\
    #         .place(relx=0.88,rely=0.00)  
    # Button(root,text="打开",font=("楷体",10),command=lambda:filepath(s,t),bg="green")\
    #         .place(relx=0.88,rely=0.00) 
    # Button(root,text="打开",font=("楷体",10),command=lambda:filepath(s,t),bg="green")\
    #         .place(relx=0.88,rely=0.00) 

menu()