# 签到免单
# 入口>京东极速版>首页>签到免单
# 脚本功能为自动签到，还在测试中
# 环境变量JD_COOKIE，多账号用&分割
# export JD_COOKIE="第1个cookie&第2个cookie"
import time
import os
import re
import requests
import sys
requests.packages.urllib3.disable_warnings()


# 随机ua
def ua_random():
    try:
        from jdEnv import USER_AGENTS as ua
    except:
        ua='jdpingou;android;5.5.0;11;network/wifi;model/M2102K1C;appBuild/18299;partner/lcjx11;session/110;pap/JA2019_3111789;brand/Xiaomi;Mozilla/5.0 (Linux; Android 11; M2102K1C Build/RKQ1.201112.002; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/92.0.4515.159 Mobile Safari/537.36'
    return ua

# 13位时间戳
def gettimestamp():
    return str(int(time.time() * 1000))

## 获取cooie
class Judge_env(object):
    ## 判断运行环境
    def getcodefile(self):
        global sys
        if '/ql' in os.path.abspath(os.path.dirname(__file__)):
            print("当前环境青龙\n")
            sys.path.append(os.path.abspath(os.path.dirname(__file__)))
        else:
            print('第三方环境\n') 
        if os.path.abspath('.') not in sys.path:
            sys.path.append(os.path.abspath('.'))

    ## 批量提取pin,输出ckkk,path,pin_list
    def main_run(self):
        self.getcodefile()
        if '/jd' in os.path.abspath(os.path.dirname(__file__)):
            cookie_list=self.v4_cookie()
        else:
            cookie_list=os.environ["JD_COOKIE"].split('&')       # 获取cookie_list的合集
        if len(cookie_list)<1:
            print('请填写环境变量JD_COOKIE\n')    
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

# 获取商品id
def sign_merch(cookie):
    url='https://api.m.jd.com/?functionId=signFreeHome&body=%7B%22linkId%22%3A%22PiuLvM8vamONsWzC0wqBGQ%22%7D&_t=1634189114026&appid=activities_platform'
    headers={
        'Host': 'api.m.jd.com',
        'accept': 'application/json, text/plain, */*',
        'origin': 'https://signfree.jd.com',
        'sec-fetch-dest': 'empty',
        'user-agent': ua,
        'x-requested-with': 'com.jd.jdlite',
        'sec-fetch-site': 'same-site',
        'sec-fetch-mode': 'cors',
        'referer': 'https://signfree.jd.com/?activityId=PiuLvM8vamONsWzC0wqBGQ&lng=107.647085&lat=30.280608&sid=2c81fdcf0d34f67bacc5df5b2a4add6w&un_area=4_134_19915_0',
        'accept-encoding': 'gzip, deflate',
        'accept-language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7',
        'cookie': cookie
    }
    for n in range(5):
        a=0
        try:
            time.sleep(2)
            res = requests.get(url=url, headers=headers, timeout=10,verify=False).json()
            a=1
            break
        except:
            print('请求失败，正在重试🌐...')
    if a!=1:
        msg('❗任务失败...')
        return False
    success=res['success']
    if not success:
        msg('请求被拒绝⭕\n')
    elif success:
        a_list=[]
        msg('获取成功✅')
        # print(res)
        if not res['data']['signFreeOrderInfoList']:
            msg('没有需要签到的商品\n')
            return False
        msg(f"共 {len(res['data']['signFreeOrderInfoList'])} 个需要签到的商品\n")
        msg('| 商品名称         | 商品id         |')
        for orderId in res['data']['signFreeOrderInfoList']:
            msg(f"| {orderId['productName']}  |  {orderId['orderId']} |")
            a_list.append(orderId['orderId'])
        msg('')
        return a_list
    else:
        msg('❗️未知错误\n')
        return False

# 签到
def sign_in(cookie,a):
    msg(f'开始签到 商品id {a} ')
    url='https://api.m.jd.com'
    headers={
        'Host': 'api.m.jd.com',
        'accept': 'application/json, text/plain, */*',
        'origin': 'https://signfree.jd.com',
        'sec-fetch-dest': 'empty',
        'user-agent': ua,
        'content-type': 'application/x-www-form-urlencoded',
        'x-requested-with': 'com.jd.jdlite',
        'sec-fetch-site': 'same-site',
        'sec-fetch-mode': 'cors',
        'referer': 'https://signfree.jd.com/?activityId=PiuLvM8vamONsWzC0wqBGQ&lng=107.647085&lat=30.280608&sid=2c81fdcf0d34f67bacc5df5b2a4add6w&un_area=4_134_19915_0',
        'accept-encoding': 'gzip, deflate',
        'accept-language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7',
        'cookie': cookie
    }
    data=f'functionId=signFreeSignIn&body=%7B%22linkId%22%3A%22PiuLvM8vamONsWzC0wqBGQ%22%2C%22orderId%22%3A{a}%7D&_t=1634183895785&appid=activities_platform'
    for n in range(3):
        a=0
        try:
            time.sleep(1)
            res = requests.post(url=url, headers=headers, data=data, timeout=2,verify=False).json()
            a=1
            break
        except:
            msg('请求失败，正在重试🌐...')
    if a!=1:
        msg('❗任务失败...')
        return False
    success=res['success']
    if not success:
        msg(f"{res['errMsg']}\n")
    elif success:
        msg('签到成功\n')
    else:
        msg('❗️未知错误\n')
        return False


# 检查账号有效性
def getUserInfo(cookie):
    try:
        pin=re.match(r'pt_key=(.+);pt_pin=(.+);', cookie).group(2)
    except:
        msg('有一个cookie 格式出错\n')
        return False
    time.sleep(0.2)
    url = 'https://me-api.jd.com/user_new/info/GetJDUserInfoUnion?orgFlag=JD_PinGou_New&callSource=mainorder&channel=4&isHomewhite=0&sceneval=2&sceneval=2&callback='
    headers = {
        'Cookie': cookie,
        'Accept': '*/*',
        'Connection': 'close',
        'Referer': 'https://home.m.jd.com/myJd/home.action',
        'Accept-Encoding': 'gzip, deflate, br',
        'Host': 'me-api.jd.com',
        'User-Agent': ua,
        'Accept-Language': 'zh-cn'
    }
    try:
        if sys.platform == 'ios':
            resp = requests.get(url=url, verify=False, headers=headers, timeout=60).json()
        else:
            resp = requests.get(url=url, headers=headers, timeout=60).json()
        if resp['retcode'] == "0":
            nickname = resp['data']['userInfo']['baseInfo']['nickname']  # 账号名
            return True
        else:
            msg(f"账号 {pin} Cookie 已失效！请重新获取。\n")
    except Exception:
        msg(f"账号 {pin} Cookie 已失效！请重新获取。\n")
    return False

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

def doTask(cookie):
    a=cookie
    if not a:
        return
    merch_list=sign_merch(cookie)
    if not merch_list:
        return
    for merch in merch_list:
        sign_in(cookie,merch)
 

if __name__ == '__main__':
    #msg('🔔签到免单，开始！\n')
    ua=ua_random()
    cookie_list=Judge_env().main_run()
    msg(f'====================共{len(cookie_list)}京东个账号Cookie=========\n')
    cookie_match=re.compile(r'pt_key=(.+);pt_pin=(.+);')
    for e,cookie in enumerate(cookie_list,start=1):
        pin=cookie_match.match(cookie).group(2)
        msg(f'******开始【账号 {e}】 {pin} *********\n')
        doTask(cookie)
