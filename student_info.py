def print_student(l):  #打印表格
    print("+"+"-"*15+"+"+"-"*11+"+"+"-"*10+"+")
    print("|"+"name".center(15)+"|"+"age".center(11)+"|"+"score".center(10)+"|")
    print("+"+"-"*15+"+"+"-"*11+"+"+"-"*10+"+")
    for d in l:
        line = ("|"+d["name"].center(15)
           +"|"+str(d["age"]).center(11)
           +"|"+str(d["score"]).center(10)+"|")
        print(line)
    print("+"+"-"*15+"+"+"-"*11+"+"+"-"*10+"+")

###############################################################################
def shanchu(l): #删除学生信息函数
    n=input('请输入要删除的学生的名称：')
    for x in range(len(l)):#遍历字典查找要删除的学生名称
        if l[x]['name']==n:#查找字典中'name'的值，索引到输入的名称
            del l[x]#删除相对应的信息
            break
    print('已删除',n,'信息')
    return l

###############################################################################
def xiugai(l):#修改学生信息函数
    n=input('请输入您要修改信息的学生名称：')
    for x in range(len(l)):
        if l[x]['name']==n:
            l[x]['name']=n
            l[x]['age']=int(input('请输入学生年龄：'))
            l[x]['score']=int(input('请输入学生成绩：'))
    print(n,'信息已修改')
    return l

###############################################################################
def chengjidaxiao(l):  # 按照成绩大小排序
    def chengji(g):  # g是字典
        return g['score'] 
    #l2 = sorted(l, key=lambda d:d['score'] 
              # reverse=True) 

    l2 = sorted(l, key=chengji, reverse=True)
    print_student(l2)


###############################################################################
def chengjixiaoda(l):  # 按照成绩xiaoda排序
    def chengji(x):  # d是字典
        return x['score']

    l2 = sorted(l, key=chengji)
    print_student(l2)


###############################################################################
def nianlingdaxiao(l):  # 按照年龄daxiao排序
    def nianlin(x):  # x是字典
        return x['age']

    l2 = sorted(l, key=nianlin,reverse= True)
    print_student(l2)


###############################################################################
def nianlingxiaoda(l):  # 按照年龄xiaoda排序
    def nianlin(x):  # d是字典
        return x['age']
    l2 = sorted(l, key=nianlin)
    print_student(l2)
