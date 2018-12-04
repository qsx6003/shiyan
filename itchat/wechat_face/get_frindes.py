import itchat
itchat.auto_login(hotReload = True)
# josn数据类型
friends = itchat.get_friends(update=True)[0:]
# print(friends[0]["NickName"])
fimle = mail = other = 0
a = 0
for ch in friends[1:]:
    # print(ch["NickName"],end =",")
    if ch["Sex"] == 1:
        mail += 1
    elif ch["Sex"] == 2:
        fimle += 1
    else:
        other += 1
    # if ch['RemarkName']== "李婷":
    print(ch)
    try:
        img = itchat.get_head_img(userName=ch["UserName"])
        with open("C:/Users/Administrator/Desktop/we_img/%s.jpg" %ch['NickName'],'wb') as f:
            f.write(img)
    except OSError:
        ch['NickName'] = "变态%d" %a
        img = itchat.get_head_img(userName=ch["UserName"])
        with open("C:/Users/Administrator/Desktop/we_img/%s.jpg" %ch['NickName'],'wb') as f:
            f.write(img)
            a +=1
# print(friends[3])
print("男好友:%d人,女好友%d人,未知%d人" %(mail,fimle,other))
print("共",len(friends[1:]),"好友")
