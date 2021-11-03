# 愤怒的锦鲤
# 入口>京东首页>券后9.9>领券>锦鲤红包
# 环境变量JD_COOKIE，多账号用&分割
# 环境变量kois中填入需要助力的pt_pin，有多个请用 '@'或'&'或空格 符号连接
# export JD_COOKIE="第1个cookie&第2个cookie"
# export kois=" 第1个cookie的pin & 第2个cookie的pin "


import os,json,random,time,re,string,functools,asyncio
import sys
sys.path.append('../../tmp')
try:
    import aiohttp
except Exception as e:
    print(e, "\n缺少aiohttp 模块，请执行命令安装: pip3 install aiohttp")
    exit(3) 


run_send='no'     # yes或no, yes则启用通知推送服务


# 获取pin
cookie_findall=re.compile(r'pt_pin=(.+?);')
def get_pin(cookie):
    try:
        return cookie_findall.findall(cookie)[0]
    except:
        print('ck格式不正确，请检查')


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

    def main(self,n=1):
        global send,msg,initialize
        sys.path.append(os.path.abspath('.'))
        for n in range(3):
            try:
                from sendNotify import send,msg,initialize
                break
            except:
                self.getsendNotify()
        l=['BARK','SCKEY','TG_BOT_TOKEN','TG_USER_ID','TG_API_HOST','TG_PROXY_HOST','TG_PROXY_PORT','DD_BOT_TOKEN','DD_BOT_SECRET','Q_SKEY','QQ_MODE','QYWX_AM','PUSH_PLUS_TOKEN','PUSH_PLUS_USER']
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
            if n < 5:
                n += 1
                return self.main(n)
            else:
                print('获取通知服务失败，请检查网络连接...')
Msg().main()   # 初始化通知服务   


async def taskPostUrl(functionId, body, cookie):
    url=f'https://api.m.jd.com/api?appid=jinlihongbao&functionId={functionId}&loginType=2&client=jinlihongbao&t={gettimestamp()}&clientVersion=10.1.4&osVersion=-1'
    headers={
        'Cookie': cookie,
        'Host': 'api.m.jd.com',
        'Connection': 'keep-alive',
        'origin': 'https://happy.m.jd.com',
        'referer': 'https://happy.m.jd.com/babelDiy/zjyw/3ugedFa7yA6NhxLN5gw2L3PF9sQC/index.html?channel=9&un_area=4_134_19915_0',
        'Content-Type': 'application/x-www-form-urlencoded',
        "User-Agent": ua(),
        'Accept-Language': 'zh-cn',
        'Accept-Encoding': 'gzip, deflate, br',
    }
    data=f"body={json.dumps(body)}"
    for n in range(3):
        try:
            async with session.post(url, headers=headers,data=data) as res:
                res =await res.text()
                return res
        except:
            if n==3:
                msg('API请求失败，请检查网路重试❗\n')  


id_findall=re.compile(r'","id":(.+?),"')
# 获取助力码
async def h5activityIndex(cookie):
    global inviteCode_list
    body={"isjdapp":1}
    res=await taskPostUrl("h5activityIndex", body, cookie)
    if not res:
        return
    inviteCode=id_findall.findall(res)
    if inviteCode:
        inviteCode=inviteCode[0]
        inviteCode_list.append(inviteCode)
        msg(f"账号 {get_pin(cookie)} 的锦鲤红包助力码为 {inviteCode}\n")
    else:
        msg(f"账号 {get_pin(cookie)} 获取助力码失败\n")


statusDesc_findall=re.compile(r',"statusDesc":"(.+?)"')
# 助力
async def jinli_h5assist(cookie,redPacketId):
    msg(f'账号 {get_pin(cookie)} 去助力{redPacketId}')
    body={"redPacketId":redPacketId,"followShop":0,"random":''.join(random.sample(string.digits, 6)),"log":"42588613~8,~0iuxyee","sceneid":"JLHBhPageh5"}
    res=await taskPostUrl("jinli_h5assist", body, cookie)
    if not res:
        return
    statusDesc=statusDesc_findall.findall(res)[0]
    if statusDesc:
        msg(f"{statusDesc}\n")
    else:
        msg(f"错误\n{res}\n")


async def asyncmain():

    debug_pin=get_env('kois')
    cookie_list_pin=[cookie for cookie in cookie_list if get_pin(cookie) in debug_pin]

    global inviteCode_list
    inviteCode_list=list()

    global session
    async with aiohttp.ClientSession() as session:

        msg('获取助力码\n')
        tasks=list()
        for cookie in cookie_list_pin:
            tasks.append(h5activityIndex(cookie))
        await asyncio.wait(tasks)

        msg('助力\n')
        tasks=list()
        for inviteCode in inviteCode_list:
            for cookie in cookie_list:
                tasks.append(jinli_h5assist(cookie,inviteCode))
        await asyncio.wait(tasks)

        
def main():
    msg('🔔愤怒的锦鲤，开始！\n')
    msg(f'====================共{len(cookie_list)}京东个账号Cookie=========\n')

    asyncio.run(asyncmain())
    
    if run_send=='yes':
        send('愤怒的锦鲤')   # 通知服务


if __name__ == '__main__':
    main()



