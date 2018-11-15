from main import input_student
from student_info import*
import time
# from menu import showmenu
def showmenu():
    print("+-----------------------+") 
    print("|   1) 添加学生信息     |") 
    print("|   2) 显示学生信息     |")
    print("|   3) 删除学生信息     |")
    print("|   4) 修改学生成绩     |")
    print("|   5) 成绩高-低排序    |")
    print("|   6) 成绩低-高排序    |")
    print("|   7) 年龄高-低排序    |")
    print("|   8) 年龄低-高排序    |")
    print("|   q)     退出         |")
    print("+-----------------------+")

def xuanze():
    baocun=[]
    while True:
        showmenu()
        s = int(input("请选择： "))
        if s == 1:#添加学生信息
            baocun += input_student()   
        elif s == 'q':
            break
        elif s == 2:# 打印表格
            print_student(baocun)
        elif s == 3: # 删除信息
            shanchu(baocun)
        elif s == 4:
            xiugai(baocun)
        elif s == 5:
            chengjidaxiao(baocun)
        elif s == 6:
            chengjixiaoda(baocun)
        elif s == 7:
            nianlingdaxiao(baocun)
        elif s == 8:
            nianlingxiaoda(baocun)
time.sleep(1)
xuanze() 