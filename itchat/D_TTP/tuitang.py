import sys
import requests
import threading
thread_lock = threading.BoundedSemaphore(value=10)


# 传入参数得到字典

def get_page(url,lib,start):
    date = {'kw':'{}'.format(lib),'limit':100,'start':start}
    r = requests.get(url,params=date)
    return r.json()
#解析字典的到图片地址
def jiexi(resul):
    l = []
    urls = resul['data']['object_list']
    for ch in urls:
       l.append(ch['photo']['path'])
    return l
# 输入关键字拿到总共的图片;改变地址 去拿到所有的图片链接
def urls(url,lib):
    l1=[]
    for start in range(0,1000,100):
        page = get_page(url,lib,start)
        l = jiexi(page)
        l1.extend(l)
    return l1

def image(ch,n,keword):

    data = requests.get(ch)
    data = data.content
    with open('D:/beauty/{}.jpg' .format(keword+str(n)),'wb') as f:
        f.write(data)
    thread_lock.release()

def main(keword):
    url = 'https://www.duitang.com/napi/blog/list/by_search/?'
    l = urls(url,keword)
    n = 0
    #创建线程
    try:
        for ch in l:
            n += 1
            print('正在下载第%d张' %n)
            thread_lock.acquire()
            t = threading.Thread(target=image,args=(ch,n,keword))
            # t.daemon = True
            t.start()
    except KeyboardInterrupt:
        sys.exit("退出")
if __name__ == "__main__":
    main('少女')