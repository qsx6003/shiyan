def cankao():#参考函数
    print("+--------------------------------+")
    print("| 1)  添加学生信息               |")
    print('| 2)  显示学生信息               |')
    print('| 3)  删除学生信息               |')
    print('| 4)  修改学生信息               |')   
    print('| q)  退出                       |')
    print('+--------------------------------+')    

def input_student():#学生信息函数
    l=[]
    while True:
        n=input('请输入姓名：')
        if not n:
            break
        a=int(input('请输入年龄：'))
        s=int(input('请输入成绩：'))
        # d={'name':n,'age':a,'score':s}
        d={}#建立字典储存每位学生的信息，等价与上一行
        d['name']=n
        d['age']=a
        d['score']=s
        l.append(d)
    return l
def output_student(l):#框架函数
    print('+'+'-'*15+'+'+'-'*9+'+'+'-'*9+'+')
    print('|'+' '*6+'name'+' '*5+'|'+' '*3+'age'+' '*3+'|'+' '*2+'score'+' '*2+'|')
    print('+'+'-'*15+'+'+'-'*9+'+'+'-'*9+'+')
    for d in l:#判断列表中的字典
        n=d['name']
        a=d['age']
        s=d['score']
        print('|%s|%s|%s|'%(n.center(15),str(a).center(9),str(s).center(9)))
    print('+'+'-'*15+'+'+'-'*9+'+'+'-'*9+'+')
# l=input_student()
# print(l)
# output_student(l)

def shanchu(l): #删除学生信息函数
    n=input('请输入要删除的学生的名称：')
    for x in range(len(l)):#遍历字典查找要删除的学生名称
        if l[x]['name']==n:#查找字典中'name'的值，索引到输入的名称
            del l[x]#删除相对应的信息
            break
    print('已删除',n,'信息')
    return l

def xiugai(l):#修改学生信息函数
    n=input('请输入您要修改信息的学生名称：')
    for x in range(len(l)):
        if l[x]['name']==n:
            l[x]['name']=n
            l[x]['age']=int(input('请输入学生年龄：'))
            l[x]['score']=int(input('请输入学生成绩：'))
    print(n,'信息已修改')
    return l
def main():
    l = []
    while True:
        cankao()#调用参考函数
        s = input("请选择: ")
        if s == 'q':
            break
        elif s == '1':
            l += input_student()#调用学生信息函数
        elif s == '2':
            output_student(l)#调用框架函数
        elif s =='3':
            shanchu(l)#调用删除信息函数
        elif s =='4':
            xiugai(l)#调用修改信息函数
main()