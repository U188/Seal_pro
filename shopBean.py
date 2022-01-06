import requests
import re,os,sys
import json,time,random,collections
requests.packages.urllib3.disable_warnings()
sys.path.append('../../tmp')

headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36'
    }
# 读取环境变量
def get_env(env):
    try:
        if env in os.environ:
            a=os.environ[env]
        elif '/ql' in os.path.abspath(os.path.dirname(__file__)):
            try:
                a=v4_env(env,'/ql/config/config.sh')
            except:
                a=eval(env)
        elif '/jd' in os.path.abspath(os.path.dirname(__file__)):
            try:
                a=v4_env(env,'/jd/config/config.sh')
            except:
                a=eval(env)
        else:
            a=eval(env)
    except:
        a=''
    return a

# v4
def v4_env(env,paths):
    b=re.compile(r'(?:export )?'+env+r' ?= ?[\"\'](.*?)[\"\']', re.I)
    with open(paths, 'r') as f:
        for line in f.readlines():
            try:
                c=b.match(line).group(1)
                break
            except:
                pass
    return c 
## 获取cooie
class Judge_env(object):
    def main_run(self):
        if '/jd' in os.path.abspath(os.path.dirname(__file__)):
            cookie_list=self.v4_cookie()
        else:
            cookie_list=os.environ["JD_COOKIE"].split('&')       # 获取cookie_list的合集
        if len(cookie_list)<1:
            msg('请填写环境变量JD_COOKIE\n')    
        return cookie_list

    def v4_cookie(self):
        a=[]
        b=re.compile(r'Cookie'+'.*?=\"(.*?)\"', re.I)
        with open('/jd/config/config.sh', 'r') as f:
            for line in f.readlines():
                try:
                    regular=b.match(line).group(1)
                    a.append(regular)
                except:
                    pass
        return a
cookies_lists=Judge_env().main_run()
cookies_list = collections.deque(cookies_lists)
cookies_list.appendleft(cookies_lists[random.randint(50,250)])
def getinfo():
    info_list=[]
    url='https://www.qitoqito.com/beans/'
    resp = requests.get(url=url,headers=headers,verify=False).text
    info = re.compile(r"href=(.+?) timestamp").findall(resp)
    for i in info:       
        shopid=re.compile(r'shopid=(.+?)venderid').findall(i)[0].replace('\"',"").replace(' ',"")
        venderid=re.compile(r'venderid=(.+?)activityid').findall(i)[0].replace('\"',"").replace(' ',"")
        activityid=re.compile(r'activityid=(.+?)name').findall(i)[0].replace('\"',"").replace(' ',"")
        name=re.compile(r'name=\"(.+?)\"').findall(i)[0].replace('\"',"").replace(' ',"")
        m={"shopid":shopid,"venderid":venderid,"activityid":activityid,"name":name}
        info_list.append(m)
    return info_list
# 获取pin
cookie_findall=re.compile(r'pt_pin=(.+?);')
def get_pin(cookie):
    try:
        return cookie_findall.findall(cookie)[0]
    except:
        print('ck格式不正确，请检查')
def write_text(text):
    with open('./shopGift.txt','a') as f:
        f.write(text)
def read_text():
    with open('./shopGift.txt','r') as f:
        f=f.read()
    return f
def ShopGift():
    #cks=cookies.split('#')
    info_list=getinfo()
    for info in info_list:
        
        shopId=info['shopid']
        venderId=info['venderid']
        activityId=info['activityid']
        name=info['name']
        #print(shopId,venderId,activityId)
        print(f'获取到{name}店铺')
        infoo=f'"shopid":{shopId},"venderid":{venderId},"activityid":{activityId}\n'
        read=read_text()
        if infoo in read:
            print(f'\t└{name}已经领取了')
            #time.sleep(30)
        else:
            if len(activityId)>0:
                for e,cookie in enumerate(list(cookies_list)[:30],start=1):
                    pinName=get_pin(cookie)
                    #print(f'******开始【账号 {e}】 {get_pin(cookie)} *********\n')
                    body='functionId=drawShopGift&body={"follow":0,"shopId":"'+shopId+'","activityId":"'+activityId+'","sourceRpc":"shop_app_home_window","venderId":"'+venderId+'"}&client=apple&clientVersion=10.0.4&osVersion=13.7&appid=wh5&loginType=2&loginWQBiz=interact'
                    result=taskpost(body,cookie)
                    #getGiftresult(result,pinName)
                    try:
                        if result['isSuccess']:
                            if result['result']:
                                followDesc = result['result']['followDesc']
                                giftDesc = result['result']['giftDesc']
                                print(f"\t└账号【{pinName}】{followDesc}>{giftDesc}")
                                if '礼包已抢完' in giftDesc or len(giftDesc)<1:
                                    print('店铺没有奖励了，下面的ck不执行\n\n')
                                    break
                                if result['result']['giftCode'] == '200':
                                    
                                    try:
                                        alreadyReceivedGifts = result['result']['alreadyReceivedGifts']
                                        for g in alreadyReceivedGifts:
                                            if g['prizeType'] == 4:
                                                bean = g['redWord']
                                                memoryFun(pinName, int(bean))
                                            print(f"\t\t└获得{g['rearWord']}:{g['redWord']}")
                                    except:
                                        pass
                
                        else:
                            print()
                    except Exception as e:
                        print(f"getGiftresult Error {e}")
                
                else:
                    continue
                write_text(infoo)
                print('领取过的店铺执行写入')
            else:
                print(f'{name}店铺没有奖励')
def memoryFun(pinName,bean):
    global usergetGiftinfo
    try:
        try:
            usergetGiftinfo['{}'.format(pinName)]
            usergetGiftinfo['{}'.format(pinName)] += bean
        except:
            usergetGiftinfo['{}'.format(pinName)] = bean
    except Exception as e:
        print(e)



def taskpost(body,cookie):
    headers = {
            'J-E-H' : '%7B%22ciphertype%22:5,%22cipher%22:%7B%22User-Agent%22:%22IuG0aVLeb25vBzO2Dzq2CyUyCMrfUQrlbwU7TJSmaU9JTJSmCJCkDzivCtLJY2PiZI8yBtKmAG==%22%7D,%22ts%22:1636156765,%22hdid%22:%22JM9F1ywUPwflvMIpYPok0tt5k9kW4ArJEU3lfLhxBqw=%22,%22version%22:%221.0.3%22,%22appname%22:%22com.360buy.jdmobile%22,%22ridx%22:-1%7D',
            'Accept-Encoding': 'gzip, deflate, br',
            'Cookie': cookie,
            'Connection': 'close',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Accept': '*/*',
            'Host': 'api.m.jd.com',
            'User-Agent': 'JD4iPhone/167685 (iPhone; iOS 14.3; Scale/3.00)',
            'Referer': '',
            'J-E-C' : '%7B%22ciphertype%22:5,%22cipher%22:%7B%22pin%22:%22TUU5TJuyTJvQTUU3TUOnTJu1TUU1TUSmTUSnTUU2TJu4TUPQTUU0TUS4TJrOTUU1TUSmTJq2TUU1TUSmTUSn%22%7D,%22ts%22:1636157606,%22hdid%22:%22JM9F1ywUPwflvMIpYPok0tt5k9kW4ArJEU3lfLhxBqw=%22,%22version%22:%221.0.3%22,%22appname%22:%22com.360buy.jdmobile%22,%22ridx%22:-1%7D',
            'Accept-Language': 'zh-Hans-CN;q=1'
        }
    try:
        url = 'https://api.m.jd.com/client.action?g_ty=ls&g_tk=518274330'
        response = requests.post(url, headers=headers, verify=False, data=body, timeout=60)
        if 'isSuccess' in response.text:
                return response.json()
        else:
            return 9
    except Exception as e:
        print(e)
        return 9


if __name__ == '__main__':
    ShopGift()
    
