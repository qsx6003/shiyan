#! python3
# -*-coding:utf-8-*-
# 下载单个post或整个博客，只实现了图片、视频
import os
import re
import json
import requests
import time
import subprocess
from six.moves import queue as Queue
from threading import Thread
import http.cookiejar as cookielib
#-------------------------------------------------------------------------------
#---------------------------------全局变量设置-----------------------------------
#多线程数量
THREADS_NUM = 10
#过墙代{过}{滤}理设置              
PROXIES = {'https': 'https://127.0.0.1:55555','http': 'http://127.0.0.1:55555'}
#网络错误重试最大次数
MAXRETRY = 20
#默认保存目录 
DEFSAVEDIR = 'E:/tumblr/'
#UA设置,复制自己浏览器的UA。当在浏览器登录后，再用这个登录，若此UA与自己浏览器的不一样，则会出现google验证，由于login函数中未实现模拟google验证，则会登录失败
HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'}
#cookies默认保存位置   
COOKIEPATH = os.path.join(DEFSAVEDIR, "Cookies.txt")
#另启一个终端显示下载线程的下载信息
CMDPROCESS = subprocess.Popen('cmd', creationflags = subprocess.CREATE_NEW_CONSOLE, stdin = subprocess.PIPE, cwd = 'd:/') 
#-------------------------------------------------------------------------------
#----------------------------------函数封装--------------------------------------
def cmd_print(printstr):
    CMDPROCESS.stdin.write(('title %s\n' % printstr).encode('utf-8'))  
    CMDPROCESS.stdin.flush()
 
def session_get(url, headers, proxies, cookies, allow_redirects = True):    
    session = requests.session()
    session.cookies = cookies
    retry = 0
    while retry < MAXRETRY:
        try:           
            return session.get(url = url, headers = headers, proxies = proxies, allow_redirects = allow_redirects)            
        except:        
            print("-->网络错误,确认网络连接正常,5秒后重试")
            time.sleep(5)        
            retry += 1
     
def session_post(url, data, headers, proxies, cookies, allow_redirects = True):    
    session = requests.session()
    session.cookies = cookies
    retry = 0
    while retry < MAXRETRY:
        try:    
            return session.post(url = url, data = data, headers = headers, proxies = proxies, allow_redirects = allow_redirects)
        except:
            print("-->网络错误,确认网络连接正常,5秒后重试")
            time.sleep(5)        
            retry += 1
         
#-------------------------------------------------------------------------------    
 
class DownloadWorker(Thread):
    def __init__(self, queue, headers, proxies):
        Thread.__init__(self)
        self.queue = queue
        self.headers = headers
        self.proxies = proxies
 
    def run(self):
        while True:
            contenturl, savepath = self.queue.get()
            self.downloadfile(contenturl, savepath)
            self.queue.task_done()            
 
    def downloadfile(self, contenturl, savepath):  
        retry = 0
        while retry < MAXRETRY:
            try:        
                with requests.get(url = contenturl, headers = self.headers, proxies = self.proxies) as respon:
                    cmd_print("downloading : %s" %contenturl)
                    with open(savepath, 'wb') as f:                                                   
                        f.write(respon.content)
                    return                   
            except:
                cmd_print("-->network error... retry 3 seconds later")
                time.sleep(3)
                retry += 1         
#---------------------------------------------------------------------------------
class TumblrScraper(object):   
    def __init__(self, headers, proxies):              
        self.headers = headers
        self.proxies = proxies
        self.sessioncookies = {}        
        self.cookiepath = COOKIEPATH 
        #postinfo = {'user':'','postid':''}
        self.postinfo = {}
        self.errlist = []
        self.taskcount= 0       
        #单个下载时，userdir为初始值DEFSAVEDIR，整个下载时为DEFSAVEDIR+username 
        self.userdir = DEFSAVEDIR                      
        self.queue = Queue.Queue()        
        self.cookielogin()
        self.scheduling()             
 
    def scheduling(self):        
        for i in range(THREADS_NUM):
            worker = DownloadWorker(queue = self.queue, headers = self.headers , proxies = self.proxies)            
            worker.daemon = True
            worker.start()        
        self.__classmain__()
 
    def getpostinfo(self, inputinfo):
        self.taskcount = 0       
        re_user = r'https://(.*?)\.'
        re_postid = r'/post/(\d+?)\D'
        #dirlist = ["video/", "photo/", "text/", "quote/", "link/", "chat/", "audio/", "ask/"]
        dirlist = ["video/", "photo/"]       
        try:
            self.postinfo['user'] = re.findall(re_user,inputinfo)[0]
            self.postinfo['postid'] = re.findall(re_postid, inputinfo + '/')[0]                         
        except:
            tumblrsession = requests.session()
            tumblrsession.cookies = self.sessioncookies
            archiveurl = 'https://{user}.tumblr.com/archive'
            testurl = archiveurl.format(user = inputinfo)            
            r = tumblrsession.get(testurl, headers = self.headers, proxies = self.proxies, allow_redirects = False)
            #https://www.tumblr.com/safe-mode?url=https%3A%2F%2Fwanglin250.tumblr.com%2Farchive
            if r.status_code == 404:
                print("-->输入的用户名有误或该用户已删除")
                return False
            else:
                try:
                    tmp = r.headers['location']
                    print("-->用户 %s 被限制网页查看,不过api仍可以获取到数据，尝试下载" %inputinfo)
                except:
                    print("-->下载用户 %s 的所有视频图片" %inputinfo)
            self.postinfo['user'] = inputinfo
            self.postinfo['postid'] = ''
            self.userdir = DEFSAVEDIR + inputinfo + '/'           
        for dir_i in dirlist:
            typedir = self.userdir + dir_i
            if not os.path.exists(typedir):
                os.makedirs(typedir)
        return True
 
    def set_err_log(self):
        tmpstr = ''
        with open(os.path.join(self.userdir, 'err.json'), 'w') as f:
            for err in self.errlist:
                tmpstr = tmpstr + err + ',\n'
            f.write(tmpstr)
         
    def cookielogin(self):        
        if (self.sessioncookies != {}):
            return
        #若session的cookie空,则看是否存在cookie文件，尝试从保存的cookie文件登录，并验证cookie的有效性
        if os.path.exists(self.cookiepath):
            tumblrsession = requests.session()
            tumblrsession.cookies = cookielib.LWPCookieJar(filename = self.cookiepath)
            tumblrsession.cookies.load()                       
            testurl = 'https://www.tumblr.com/dashboard'
            r = session_get(testurl, headers = self.headers, proxies = self.proxies, cookies = tumblrsession.cookies, allow_redirects = False)
            try:
                r.headers['location']
                #若存在重定向，则登录过期
                print("-->cookies已过期，重新登录......")
                self.login()
            except:
                self.sessioncookies = tumblrsession.cookies
                print("-->从保存的cookie登录成功......")                
        else:
            self.login()
         
    def login(self):        
        success = False
        login_method = '0'
        cookie_dict = {} 
        cookie_jar = requests.utils.cookiejar_from_dict(cookie_dict)
        re_form_key = r'form_key" content="(.*?)"'
        #form_key在第一次登陆返回的content中，服务端会验证."g-recaptcha":谷歌验证api返回的键值，未添加
        postdata={'determine_email': '',
                'user[email]': '',
                'user[password]': '',
                'tumblelog[name]': '',
                'user[age]': '',
                'context': 'login',
                'version': 'STANDARD',
                'follow': '',
                'http_referer': 'https://www.tumblr.com/login',
                'form_key': '',
                'seen_suggestion': '0',
                'used_suggestion': '0',
                'used_auto_suggestion': '0',
                'about_tumblr_slide':'' ,
                'random_username_suggestions': '',
                'action': 'signup_determine'
        }
        postdata['determine_email'] = postdata['user[email]'] = input("用户邮件地址:")
        postdata['user[password]'] = input("密码:") 
        tumblrsession = requests.session()
        tumblrsession.cookies = cookielib.LWPCookieJar(filename = self.cookiepath) 
        html_text = tumblrsession.post(postdata['http_referer'], data = postdata, headers = self.headers, proxies = self.proxies).text
        postdata['form_key'] = re.findall(re_form_key,html_text)[0]   
        while(success == False):
            if login_method == '0':           
                r = tumblrsession.post(postdata['http_referer'], data = postdata, headers = self.headers, proxies = self.proxies, allow_redirects = False)
            else:
                testurl = 'https://www.tumblr.com/dashboard'
                r = requests.get(testurl, headers = self.headers, cookies = cookie_dict, proxies = self.proxies, allow_redirects = False)          
            try:
                r.headers['location']            
            except KeyError:
                #若不存在重定向，则表示从cookie登录成功；而从用户名密码登录则表示失败
                if login_method == '1':
                    print("-->从输入的cookie登录成功......")
                    self.sessioncookies = cookie_jar
                    #保存输入的cookie到文件,以备下次调用。----手动输入的cookie保存后采用cookielib.LWPCookieJar类来读取到session有问题
                    #new_cookie_jar = cookielib.LWPCookieJar(filename = self.cookiepath)
                    #requests.utils.cookiejar_from_dict(cookie_dict = cookie_dict, cookiejar = new_cookie_jar, overwrite = True)
                    #new_cookie_jar.save(filename = self.cookiepath, ignore_discard = True, ignore_expires = True)
                    success = True                  
                else:
                    print("-->密码或用户名错误，重新登录.若确定都正确,则是google验证问题，先在浏览器登陆或退出再登录过掉google验证")
                    login_method = input("继续选择登录方式(0=输入账号密码,1=复制浏览器cookie登录):")
                    if login_method == '0':
                        postdata['determine_email'] = postdata['user[email]'] = input("用户邮件地址:")
                        postdata['user[password]'] = input("密码:")                   
                    elif login_method == '1':
                        cookie_str = input("复制浏览器登录成功后的页面请求Request Headers中的cookie:")
                        cookie_dict = dict([item.split('=', 1) for item in cookie_str.split('; ')])
                        cookie_jar = requests.utils.cookiejar_from_dict(cookie_dict = cookie_dict, cookiejar = None, overwrite = True)
                    else:
                        print("-->登录方式输入有误")
                        login_method = '0'
            else:
                success = True
                print("-->用户名密码方式登录成功......")        
                self.sessioncookies = tumblrsession.cookies    
                tumblrsession.cookies.save()
     
    #下载video文件命名规则为:原始postusername + postid
    def getvideo_url(self, jsondata):
        try:                
            video_url = jsondata['video_url']
         #一般都是被彻底删除了       
        except KeyError:
            print("jsondata 中 video_url 不存在,加入errlist")            
            dict_err = {'posturl':jsondata['post_url'], 'reblog_from_url':jsondata['reblogged_from_tumblr_url']}
            str_err = json.dumps(dict_err, ensure_ascii=False)
            self.errlist.append(str_err)            
            #尝试从thumbnail_url获取
            try:            
                tailstr = jsondata['thumbnail_url'].split('/')[-1]            
                video_url = 'https://vtt.tumblr.com/' + tailstr.split('_frame1')[0] + '.mp4'
            except:
                return False         
        #获取post原始用户名
        try:
            reblogged_root_name = jsondata['reblogged_root_name']                    
        except KeyError:
            reblogged_root_name = self.postinfo['user']
        filename = reblogged_root_name + '_' +  str(jsondata['root_id']) + '.mp4'       
        savedir = self.userdir + "video/"      
        savepath = os.path.join(savedir, filename)
        #判重在这个类实现，便于统计下载数量
        if os.path.exists(savepath):
            return False
        print("-->下载类型为视频,保存在%s" %savepath)      
        self.queue.put((video_url, savepath))
        self.taskcount += 1
        return True
    #下载photos文件命名规则为:原始postusername + 图片本身文件名 
    def getphoto_url(self, jsondata):              
        try:
            reblogged_root_name = jsondata['reblogged_root_name']                   
        except KeyError:
            reblogged_root_name = self.postinfo['user']
        try:            
            photo_list = jsondata['photoset_photos']
        except:
            photo_list = jsondata['photos']
        for item in photo_list:
            try:
                photo_url = item['high_res']
            except:
                photo_url = item['original_size']['url']
            filename = reblogged_root_name + '_' + photo_url.split('/')[-1]
            savedir = self.userdir + "photo/"          
            savepath = os.path.join(savedir, filename) 
            if os.path.exists(savepath):
                pass
            else:      
                print("-->下载类型为图片,保存在%s" %savepath)        
                self.queue.put((photo_url, savepath))
                self.taskcount += 1
        return True
    #根据json返回的 jsondata['type'] == 'text'，但内容却可以是其他的
    def get_text_url(self, jsondata):              
        try:
            reblogged_root_name = jsondata['reblogged_root_name']                    
        except KeyError:
            reblogged_root_name = self.postinfo['user']
        try:
            bodyhtml_text = jsondata['body']
        except KeyError:
            print("-->该text类型不存在'body'键,重新查看返回json数据......")
            return False
        re_type = r'{"type":"(.*?)"'
        re_video = r'<source src="(.*?)"'
        re_img = r'<img src="(.*?)"'
        typelist = re.findall(re_type, bodyhtml_text)
        imglist = re.findall(re_img, bodyhtml_text)
        if typelist !=[]:
            body_type = typelist[0]
            #从内容确定是视频
            if body_type == 'video':               
                try:
                    video_url = re.findall(re_video, bodyhtml_text)[0]
                except:
                    print("-->jsondata['body']中存在type =='video',但未找到下载地址,用户=%s,postid=%d" %(self.postinfo['user'], jsondata['id']))
                    return False
                else:                   
                    filename = reblogged_root_name + '_' + str(jsondata['root_id']) + '.mp4'
                    savedir = self.userdir + "video/"          
                    savepath = os.path.join(savedir, filename) 
                    if not os.path.exists(savepath):                        
                        print("-->下载类型为自定义中的视频，保存在%s" %savepath)       
                        self.queue.put((video_url, savepath))
                        self.taskcount += 1
            else:
                print("-->jsondata['body']中存在type且!='video',type=%s,用户=%s,postid=%d" %(body_type, self.postinfo['user'], jsondata['id']))
                return False
        else:
            #从内容确定是图片
            if imglist != []:                
                for photo_url in imglist:                                           
                    filename = reblogged_root_name + '_' + photo_url.split('/')[-1]                    
                    savedir = self.userdir + "photo/"          
                    savepath = os.path.join(savedir, filename)
                    if not os.path.exists(savepath):                   
                        print("-->下载类型为自定义中的视频，保存在%s" %savepath)       
                        self.queue.put((photo_url, savepath))
                        self.taskcount += 1
            else:
                print("-->jsondata['body']中类型非视频、图片，未实现下载，查看json数据")
                return False
        return True   
 
    def getchat_url(self, jsondata):
        print("-->下载类型为chat,待实现......")
        return True
    def getaudio_url(self, jsondata):
        print("-->下载类型为audio,待实现......")
        return True
    def getask_url(self, jsondata):
        print("-->下载类型为ask,待实现......")
        return True
    def getquote_url(self, jsondata):
        print("-->下载类型为quote,待实现......")
        return True
    def getlink_url(self, jsondata):
        print("-->下载类型为link,待实现......")
        return True
         
    def handle_post_type(self, retjson):
        for singelpost in retjson['response']['posts']:
            content_type = singelpost['type']
            #根据json中返回类型调用相应下载链接获取函数
            '''
            switcher = {'video': self.getvideo_url(retjson),
                        'photo': self.getphoto_url(retjson),
                        'text': self.gettext_url(retjson),
                        'quote': self.getquote_url(retjson),
                        'audio': self.getaudio_url(retjson),
                        'ask': self.getask_url(retjson),
                        'link': self.getlink_url(retjson),
                        'chat': self.getchat_url(retjson),
            }.get(content_type,False)
            if switcher == False:
                print("-->json data error......")
            '''
            if content_type == 'video':
                self.getvideo_url(singelpost)
            elif content_type == 'photo':
                self.getphoto_url(singelpost)
            elif content_type == 'text':
                self.get_text_url(singelpost)
            elif content_type == 'quoto':
                self.getquote_url(singelpost)
            elif content_type == 'audio':
                self.getaudio_url(singelpost)
            elif content_type == 'answer':
                self.getask_url(singelpost)
            elif content_type == 'link':
                self.getlink_url(singelpost)
            elif content_type == 'chat':
                self.getchat_url(singelpost)
            else:
                print("-->json data error......")            
 
    # 获取 jsondata
    def get_post_json(self):
        newheaders = {'Host': 'www.tumblr.com',
                      'Connection': 'keep-alive',
                      'Accept': 'application/json, text/javascript, */*; q=0.01',
                      'X-Requested-With': 'XMLHttpRequest',              
                      'Referer': 'https://www.tumblr.com/dashboard'}
        newheaders.update(self.headers)           
        #构造json接口apiurl        
        apiurl = "https://www.tumblr.com/svc/indash_blog?tumblelog_name_or_id={user}&post_id={postid}&limit={limit}&offset={offset}&should_bypass_safemode_forpost=false\
                  &should_bypass_safemode_forblog=false&should_bypass_tagfiltering=false&can_modify_safe_mode=true"        
        #为整个博客下载
        if self.postinfo['postid'] == '':
            postid, limit, offset = '', '10', '0'   #limit默认是一次下拉10个post，设置大一些也正常返回
            retposts_lenth = 10
            while retposts_lenth == int(limit):
                svcurl = apiurl.format(user = self.postinfo['user'], postid = postid, limit = limit, offset = offset)                
                retjson = session_get(svcurl, headers = newheaders, proxies = self.proxies, cookies = self.sessioncookies).json()                    
                if retjson['meta']['status'] != 200:
                    print("-->json接口返回错误......")
                    return False
                self.handle_post_type(retjson)
                retposts_lenth = len(retjson['response']['posts'])
                offset = str(int(offset) + int(limit))
            self.set_err_log()  
        #单个post下载
        else:                    
            svcurl = apiurl.format(user = self.postinfo['user'], postid = self.postinfo['postid'], limit = '1', offset = '0')
            retjson = session_get(svcurl, headers = newheaders, proxies = self.proxies, cookies = self.sessioncookies).json()
            self.handle_post_type(retjson)
            if retjson['meta']['status'] != 200:
                    print("-->json接口返回错误......")
                    return False
        return True     
         
    def __classmain__(self):                    
        while True:
            print('---------------------------------------------------------------------------------------------------------------------' +
                  '\n-->单个格式:archive中单个右键或notes右键复制链接,或分享->转至固定链接->右键复制得到的posturl')
            inputinfo = input('---------------------------------------------------------------------------------------------------------------------' +
                              '\n-->单个下载粘贴单个posturl，整个下载粘贴博主名字:')                
            if self.getpostinfo(inputinfo) == True:                
                self.get_post_json()
                #self.queue.join()  异步添加任务到队列不启用
                print('---------------------------------------------------------------------------------------------------------------------' +
                    '\n-->用户 %s: 共 %d 项加入下载队列,等待下载完成。可继续下载其他用户文件' %(self.postinfo['user'], self.taskcount))                
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
if __name__ == "__main__":      
    if not os.path.exists(DEFSAVEDIR):
        os.makedirs(DEFSAVEDIR)
    cmd_print('threads console')    
    TumblrScraper(headers = HEADERS, proxies = PROXIES)