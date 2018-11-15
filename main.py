def input_student():  # 获取学生列表信息
    l=[]
    while True:
        n = input("请输入姓名： ")
        if n == '':
            break
        #输入年龄，输入错误就重新输入，没错就跳出循环
        while True:
            try:
                a =int(input("请输入年龄： "))
            except:
                continue
            else:
                break
        try:
            s = int(input("请输入成绩： "))
        except ValueError:
            print("错误，重新输入")
            continue
        d={}
        d['name']= n 
        d['age']= a
        d['score']= s
        l.append(d)
    return(l)
