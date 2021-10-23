# 双11活动>双11随机红包助力
# 入口>京东>首页
# 脚本功能为内部邀请，内部进团,5人一团，多于5人将跳过当前团
# 环境变量JD_COOKIE，多账号用&分割
# export JD_COOKIE="第1个cookie&第2个cookie"

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

# 获取队伍邀请码
def travel_pk_getHomeData(cookie):
    msg(f'账号{get_pin(cookie)}获取组队竞猜队伍邀请码...')
    body = {}
    res=taskPostUrl("travel_pk_getHomeData", body, cookie)
    if not res:
        return
    if res['code']==0 :
        if res['data']['bizCode'] == 0:
            try:
                inviteId=res['data']['result']['groupInfo']['groupJoinInviteId']
                msg(f"用户 {get_pin(cookie)} 的组队竞猜队伍邀请码为：{inviteId}\n")
                inviteId_list.append(inviteId) 
            except:
                msg('找不到组队竞猜队伍邀请码，快去买买买吧\n')
        else:
            msg(f"{res['data']['bizMsg']}\n")
    else:
        msg('错误')
        msg(f'{res}\n')

# 获取队伍人数
def travel_pk_getHomeData_2(cookie):
    body = {}
    res=taskPostUrl("travel_pk_getHomeData", body, cookie)
    if not res:
        return
    if res['code']==0 :
        if res['data']['bizCode'] == 0:
            try:
                userNickName=len(res['data']['result']['groupInfo']['memberList'])
                msg(f"用户 {get_pin(cookie)} 的团人数为：{userNickName}\n")
                return userNickName
            except:
                msg('获取团人数失败，快去买买买吧\n')
        else:
            msg(f"{res['data']['bizMsg']}\n")
    else:
        msg('错误')
        msg(f'{res}\n')


# 助力
def travel_pk_joinGroup(cookie,inviteId):
    msg(f'账号 {get_pin(cookie)} 去助力{inviteId}')
    body = { "inviteId":inviteId,"confirmFlag":"1", "ss": { "extraData": { "log": "", "sceneid": "HYJhPageh5" }, "secretp": get_secretp(cookie), "random": ''.join(random.sample(string.digits, 6)) }, "inviteId": inviteId }
    res=taskPostUrl("travel_pk_joinGroup", body, cookie)
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
    msg('🔔双11随机红包助力，开始！\n')
    global inviteId_list
    inviteId_list=[]
    msg(f'====================共{len(cookie_list)}京东个账号Cookie=========\n')
    msg(f'5人1团，将获取前{len(cookie_list)//5}个账号的队伍邀请码\n')
    msg(f'5人1团，将获取前{len(cookie_list)//5}个账号的队伍邀请码\n')
    msg(f'5人1团，将获取前{len(cookie_list)//5}个账号的队伍邀请码\n')
    for e,cookie in enumerate(cookie_list,start=1):
        msg(f'******开始【账号 {e}】 {get_pin(cookie)} *********\n')
        if not getUserInfo(cookie):
            continue
        travel_pk_getHomeData(cookie)
        if e==(len(cookie_list)//5):
            break
    
    for f,inviteId in enumerate(inviteId_list,start=1):
        try:
            if travel_pk_getHomeData_2(cookie_list[f-1])>=5:
                msg('跳过该账号\n')
                continue
            for e,cookie in enumerate(cookie_list,start=1):
                if travel_pk_getHomeData_2(cookie_list[f-1])>=5:
                    msg('跳过该账号\n')
                    break
                if not travel_pk_joinGroup(cookie,inviteId):
                    if not f==e:
                        msg(f'账号{get_pin(cookie)}火爆或助力次数已耗尽，跳过该账号\n')
                        break
        except:
            msg('黑号吧\n')
    if run_send=='yes':
        send('### 组队竞猜赢大奖 ###')   # 通知服务


if __name__ == '__main__':
    main()

