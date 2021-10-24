# 双11活动>天降红包助力
# 入口>京东>首页
# 也许是天降红包助力，说不准说不准
# 脚本功能为助力，先运行一次脚本查看助力码，再把需要助力的脚本放在环境变量里
# 环境变量JD_COOKIE，wy_11tjhb多账号用&分割
# export JD_COOKIE="第1个cookie&第2个cookie"
# export wy_11tjhb="助力码1&助力码2"

import os,json,random,time,re,string
import sys
sys.path.append('../../tmp')
try:
    import requests
except Exception as e:
    msg(str(e) + "\n缺少requests模块, 请执行命令：pip3 install requests\n")
requests.packages.urllib3.disable_warnings()


JD_API_HOST = 'https://api.m.jd.com/client.action'
run_send='no'     # yes或no, yes则启用通知推送服务


cookie_match=re.compile(r'pt_key=(.+);pt_pin=(.+);')
def get_pin(cookie):
    return cookie_match.match(cookie).group(2)

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
        a=False
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

# 随机ua
def ua():
    sys.path.append(os.path.abspath('.'))
    try:
        from jdEnv import USER_AGENTS as a
    except:
        a='jdpingou;android;5.5.0;11;network/wifi;model/M2102K1C;appBuild/18299;partner/lcjx11;session/110;pap/JA2019_3111789;brand/Xiaomi;Mozilla/5.0 (Linux; Android 11; M2102K1C Build/RKQ1.201112.002; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/92.0.4515.159 Mobile Safari/537.36'
    return a

# 13位时间戳
def gettimestamp():
    return str(int(time.time() * 1000))

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
cookie_list=Judge_env().main_run()

# 检查账号有效性
def getUserInfo(cookie):
    try:
        pin=get_pin(cookie)
    except:
        msg('有一个cookie 格式出错\n')
        return
    time.sleep(0.2)
    url = 'https://me-api.jd.com/user_new/info/GetJDUserInfoUnion?orgFlag=JD_PinGou_New&callSource=mainorder&channel=4&isHomewhite=0&sceneval=2&sceneval=2&callback='
    headers = {
        'Cookie': cookie,
        'Accept': '*/*',
        'Connection': 'close',
        'Referer': 'https://home.m.jd.com/myJd/home.action',
        'Accept-Encoding': 'gzip, deflate, br',
        'Host': 'me-api.jd.com',
        'User-Agent': ua(),
        'Accept-Language': 'zh-cn'
    }
    try:
        resp = requests.get(url=url, headers=headers, timeout=60).json()
        if resp['retcode'] == "0":
            nickname = resp['data']['userInfo']['baseInfo']['nickname']  # 账号名
            return True
        else:
            msg(f"账号 {pin} Cookie 已失效！请重新获取。\n")
    except Exception:
        msg(f"账号 {pin} Cookie 已失效！请重新获取。\n")
    return


## 获取通知服务
class Msg(object):
    def getsendNotify(self, a=1):
        try:
            url = 'https://ghproxy.com/https://raw.githubusercontent.com/wuye999/myScripts/main/sendNotify.py'
            response = requests.get(url,timeout=3)
            with open('sendNotify.py', "w+", encoding="utf-8") as f:
                f.write(response.text)
            return
        except:
            pass
        if a < 5:
            a += 1
            return self.getsendNotify(a)

    def main(self):
        global send,msg,initialize
        sys.path.append(os.path.abspath('.'))
        for n in range(3):
            try:
                from sendNotify import send,msg,initialize
                break
            except:
                self.getsendNotify()
        l=['BARK','PUSH_KEY','TG_BOT_TOKEN','TG_USER_ID','TG_API_HOST','TG_PROXY_HOST','TG_PROXY_PORT','DD_BOT_TOKEN','DD_BOT_SECRET','QQ_SKEY','Q_SKEY','QQ_MODE','QYWX_AM','PUSH_PLUS_TOKEN']
        d={}
        for a in l:
            try:
                d[a]=eval(a)
            except:
                d[a]=''
        try:
            initialize(d)
        except:
            self.getsendNotify()
            self.main()          
Msg().main()   # 初始化通知服务 


def taskPostUrl(functionId, body, cookie, resp=True):
    url=f'{JD_API_HOST}?functionId={functionId}'
    data=f'functionId={functionId}&body={body}&client=wh5&clientVersion=1.0.0'
    headers={
        'Cookie': cookie,
        'Host': 'api.m.jd.com',
        'Connection': 'keep-alive',
        'Content-Type': 'application/x-www-form-urlencoded',
        "User-Agent": ua(),
        'Accept-Language': 'zh-cn',
        'Accept-Encoding': 'gzip, deflate, br',
    }
    if resp:
        for n in range(3):
            try:
                res = requests.post(url=url, headers=headers, json=data, timeout=10,verify=False).json()
                return res
            except:
                if n==3:
                    msg('API请求失败，请检查网路重试❗\n')  
    else:
        return url,data,headers

def taskPostUrl2(functionId, body, cookie, resp=True):
    url=f'{JD_API_HOST}?functionId={functionId}&client=wh5'
    data=f'body={body}'
    headers={
        'Cookie': cookie,
        'Host': 'api.m.jd.com',
        'Connection': 'keep-alive',
        'Content-Type': 'application/x-www-form-urlencoded',
        "User-Agent": ua(),
        'Accept-Language': 'zh-cn',
        'Accept-Encoding': 'gzip, deflate, br',
    }
    if resp:
        for n in range(3):
            try:
                res = requests.post(url=url, headers=headers, json=data, timeout=10,verify=False).json()
                return res
            except:
                if n==3:
                    msg('API请求失败，请检查网路重试❗\n')      
    else:
        return url,data,headers

# 获取 secretp
def get_secretp(cookie):
    body = {}
    res=taskPostUrl("travel_getHomeData", body, cookie)
    if not res:
        return
    try:
        secretp=res['data']['result']['homeMainInfo']['secretp']
        return secretp
    except:
        msg('错误\n')
        msg(res) 

# 获取助力码
def travel_getDropRedpacketDetail(cookie):
    msg(f'账号{get_pin(cookie)}获取天降红包助力码...')
    body = {}
    res=taskPostUrl("travel_getDropRedpacketDetail", body, cookie)
    if not res:
        return
    if res['code']==0 :
        if res['data']['bizCode'] == 0:
            try:
                inviteId=res['data']['result']['inviteId']
                msg(f"用户 {get_pin(cookie)} 的天降红包助力码为：{inviteId}\n")
            except:
                msg(f"{res['data']['bizMsg']}\n")
        else:
            msg(f"{res['data']['bizMsg']}\n")
    else:
        msg('错误')
        msg(f'{res}\n')


# 助力
def travel_doDropTask(cookie,inviteId):
    msg(f'账号 {get_pin(cookie)} 去助力{inviteId}')
    body = {"ss": { "extraData": { "log": "", "sceneid": "HYJhPageh5" }, "secretp": get_secretp(cookie), "random": ''.join(random.sample(string.digits, 6)) }, "inviteId": inviteId }
    res=taskPostUrl("travel_doDropTask", body, cookie)
    if not res:
        return
    if res['code']==0 :
        if res['data']['success']:
            msg(f"助力成功✅\n")
            return True   
        else:
            msg(f"{res['data']['bizMsg']}\n")
    else:
        msg('错误')
        msg(f'{res}\n')


def main():
    msg('🔔也许是双11天降红包助力助力，开始！\n')
    inviteId_list=get_env('tjhb')
    if inviteId_list:
        inviteId_list=inviteId_list.split('&')
    msg(f'====================共{len(cookie_list)}京东个账号Cookie=========\n')

    for e,cookie in enumerate(cookie_list,start=1):
        msg(f'******开始【账号 {e}】 {get_pin(cookie)} *********\n')
        #if not getUserInfo(cookie):
            #continue
        travel_getDropRedpacketDetail(cookie)
        time.sleep(10)
    if inviteId_list:
        for f,inviteId in enumerate(inviteId_list,start=1):
            for e,cookie in enumerate(cookie_list,start=1):
                travel_doDropTask(cookie,inviteId)

    if run_send=='yes':
        send('### 也许是天降红包助力 ###')   # 通知服务


if __name__ == '__main__':
    main()
