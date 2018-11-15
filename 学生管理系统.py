# 1. 任意输入多个学生的姓名,年龄,成绩,每个学生信息存入一个字典中,然后再放入列表中(每个学生信息需要手动输入)
# 如:
#     请输入姓名: tarena
#     请输入年龄: 15
#     请输入成绩: 99
#     请输入姓名: name2
#     请输入年龄: 22
#     请输入成绩: 100
#     请输入姓名: <直接回车结束输入>
# 在程序内部生成如下列表:
# L = [{'name': tarena, 'age':15, 'score': 99}, {'name': name2, 'age':22, 'score': 100}]
# 1) 打印出上述列表
# 2) 以下列表格的形式打印出上述信息
# +---------------+-----------+----------+
# |     name      |    age    |  score   |
# +---------------+-----------+----------+
# |    tarena     |    15     |    99    |
# |     name2     |    22     |   100    |
# +---------------+-----------+----------+

# L = []  # 创建一个列表,准备用来保存学生信息的字典


# # 循环输入学生姓名,年龄,成绩,姓名为空结束输入
# #  
# while True:
#     n = input("请输入姓名: ")
#     if not n:  # 姓名为空结束输入
#         break
#     a = int(input("请输入年龄: "))
#     s = int(input("请输入成绩: "))
#     # 得到的数据形成字典,
#     d = {} # 创建一个字典
#     d['name'] = n
#     d['age'] = a
#     d['score'] = s
#     L.append(d)# 加到列表内
    

# print(l)
# print("+---------------+-----------+----------+")
# print("|     name      |    age    |  score   |")
# print("+---------------+-----------+----------+")

# for d in L:  # d绑定的是字典
#     line = '|' + d['name'].center(15)
#     line += '|' + str(d['age']).center(11)
#     line += '|' + str(d['score']).center(10)
#     line += '|'+"name".center()
#     print(line)

# # print("|    tarena     |    15     |    99    |")
# # print("|     name2     |    22     |   100    |")
# print("+---------------+-----------+----------+")



# 2.0. 改写之前的学生信息管理程序:
#      改为用两个函数实现
#        1)写函数input_student() 来获取学生信息,当输入姓名为空时结束输入.形成字典组成的列表并返回
#        2) 写函数print_student(L) 将上述函数得到的打印成为表格显示
#     如:
#       def input_student():
#           ...
#       def print_student(L):
#           ... 
#       L = input_student()  # 获取列表
#       print(L)
#       print_student(L)  # 打印表格
def input_student():
    l=[]
    while True:
        n = input("请输入姓名： ")
        if n == '':
            break
        a = input("请输入年龄： ")
        s = input("请输入成绩： ")
        d={}
        d['name']= n 
        d['age']= a
        d['score']= s
        l.append(d)
    return(l)

def print_student(l):
    print("+"+"-"*15+"+"+"-"*11+"+"+"-"*10+"+")
    print("|"+"name".center(15)+"|"+"age".center(11)+"|"+"score".center(10)+"|")
    print("+"+"-"*15+"+"+"-"*11+"+"+"-"*10+"+")
    for d in l:
        line = ("|"+d["name"].center(15)
           +"|"+str(d["age"]).center(11)
           +"|"+str(d["score"].center(10)+"|"))
        print(line)
    print("+"+"-"*15+"+"+"-"*11+"+"+"-"*10+"+")



# 3.0.实现带界面的学生信息管理系统的项目
#     +-----------------------+
#     | 1) 添加学生信息         |
#     | 2) 显示学生信息         |
#     | 3) 删除学生信息         |
#     | 4) 修改学生成绩         |
#     | q) 退出                |
#     +-----------------------+
#     (要求:用函数来实现,每个功能写一个函数写之相对应)

        # print("+----------------------+") 
        # print("|   1) 添加学生信息     |") 
        # print("|   2) 显示学生信息     |")
        # print("|   3) 删除学生信息      |")
        # print("|   4) 修改学生成绩      |")
        # print("|   5) 退出             |")
        # print("+----------------------+")
def xuanze():
    baocun=[]
    while True:
        print("+----------------------+") 
        print("|   1) 添加学生信息    |") 
        print("|   2) 显示学生信息    |")
        print("|   3) 删除学生信息    |")
        print("|   4) 修改学生成绩    |")
        print("|   5) 退出            |")
        print("+----------------------+")
        s = int(input("请选择： "))
        if s == 1:#添加学生信息
            baocun += input_student()
        elif s == 2:
            print_student(baocun)
        elif s == 3:
            print("删除学生信息")
        elif s == 4:
            print("修改学生成绩")
        elif s == 5:
            print("退出")
            break
        

            
xuanze() 

       



                     
   
