import requests
def get_response(msg):
    apiUrl = 'http://www.tuling123.com/openapi/api'
    KEY = 'd5f09b9ea887400185658545f3e1db39'
    data = {
        'key'    : KEY,
        'info'   : msg,
        'userid' : '空空'
    }
    
    try:
        r = requests.post(apiUrl, data=data).json()

        return r.get('text')
    except:
        return

def chat(a):
    while True:
        if a == 0:
            print("TL: ",get_response("我来啦"))
        else:
            tt = get_response(input("MY: "))        
            print("TL: ",tt)
        a = 1
if __name__ == "__main__":
    chat(0)

