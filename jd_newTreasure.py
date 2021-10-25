# 发现新宝藏
# 入口>   京东>12.0:/￥J5iAk3pzZUJgE4%，复制口令进入京东APP给我助力，一起瓜分1亿京豆！
# 脚本功能为 完成全部任务，内部互助，没写抽奖
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


JD_API_HOST = 'https://api.m.jd.com'
run_send='yes'     # yes或no, yes则启用通知推送服务


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
    url=f'{JD_API_HOST}/{functionId}?appid=contenth5_common&functionId={functionId}&body=[{json.dumps(body)}]'
    headers={
        'Cookie': cookie,
        'Host': 'api.m.jd.com',
        'Connection': 'keep-alive',
        'origin': 'https://prodev.m.jd.com',
        'Content-Type': 'application/x-www-form-urlencoded',
        "User-Agent": ua(),
        'Accept-Language': 'zh-cn',
        'Accept-Encoding': 'gzip, deflate, br',
    }
    if resp:
        for n in range(3):
            try:
                res = requests.get(url=url, headers=headers, timeout=10,verify=False).json()
                return res
            except:
                if n==3:
                    print('API请求失败，请检查网路重试❗\n')  
    else:
        return url,data,headers


def taskPostUrl_2(functionId, body, cookie, resp=True):
    url=f'{JD_API_HOST}/{functionId}?appid=contenth5_common&functionId={functionId}&body={json.dumps(body)}'
    headers={
        'Cookie': cookie,
        'Host': 'api.m.jd.com',
        'Connection': 'keep-alive',
        'origin': 'https://prodev.m.jd.com',
        'Content-Type': 'application/x-www-form-urlencoded',
        "User-Agent": ua(),
        'Accept-Language': 'zh-cn',
        'Accept-Encoding': 'gzip, deflate, br',
    }
    if resp:
        for n in range(3):
            try:
                res = requests.get(url=url, headers=headers, timeout=10,verify=False).json()
                return res
            except:
                if n==3:
                    print('API请求失败，请检查网路重试❗\n')  
    else:
        return url,data,headers


def taskPostUrl_3(functionId, body, cookie, resp=True):
    url=f'{JD_API_HOST}/{functionId}?appid=contenth5_common&functionId={functionId}&body=[{json.dumps(body)}]&client=wh5'
    headers={
        'Cookie': cookie,
        'Host': 'api.m.jd.com',
        'Connection': 'keep-alive',
        'origin': 'https://prodev.m.jd.com',
        'Content-Type': 'application/x-www-form-urlencoded',
        "User-Agent": ua(),
        'Accept-Language': 'zh-cn',
        'Accept-Encoding': 'gzip, deflate, br',
    }
    if resp:
        for n in range(3):
            try:
                res = requests.get(url=url, headers=headers, timeout=10,verify=False).json()
                return res
            except:
                if n==3:
                    print('API请求失败，请检查网路重试❗\n')  
    else:
        return url,data,headers

def taskPostUrl_4(functionId, body, cookie, resp=True):
    url=f'{JD_API_HOST}/{functionId}?appid=contenth5_common&functionId={functionId}&body={json.dumps(body)}&client=wh5'
    headers={
        'Cookie': cookie,
        'Host': 'api.m.jd.com',
        'Connection': 'keep-alive',
        'origin': 'https://prodev.m.jd.com',
        'Content-Type': 'application/x-www-form-urlencoded',
        "User-Agent": ua(),
        'Accept-Language': 'zh-cn',
        'Accept-Encoding': 'gzip, deflate, br',
    }
    if resp:
        for n in range(3):
            try:
                res = requests.get(url=url, headers=headers, timeout=10,verify=False).json()
                return res
            except:
                if n==3:
                    print('API请求失败，请检查网路重试❗\n')  
    else:
        return url,data,headers


# 获取活动信息
def task_assignment(cookie,assignmentId,projectId,advGrpId1,advGrpId2):
    msg(f"获取活动信息🔎...")
    body={"type":"12","projectId":projectId,"assignmentId":assignmentId,"agid":[advGrpId1,advGrpId2]}
    res=taskPostUrl("interactive_info", body, cookie)
    if not res:
        return
    if res['code']=='0' :
        if res['success']:
            try:
                msg(f"获取活动信息成功✅")
                # print(f"data数量 {len(res['data'])}")
                msg(f"活动名称：{res['data'][0]['specialName']}📑")
                msg(f"共 {len(res['data'][0]['skuList'])} 个子任务\n")
                return [res['data'][0]['assignmentId'],res['data'][0]['projectId'],res['data'][0]['skuList']]
            except:
                msg(f"找到 0 个活动信息\n")
        else:
            msg(f"找到 0 个活动信息\n")
    else:
        msg('错误⭕')
        msg(f'{res}\n')



# 分配子任务
def skuList_task(cookie,assignmentId,projectId,skuList):
    for sku in skuList:
        body={"type":"12","agid":[sku['agid']],"adid":sku['adid'],"projectId":projectId,"assignmentId":assignmentId}
        msg(f"开始 {sku['name']}📑")
        res=taskPostUrl_2("interactive_done", body, cookie)
        if not res:
            return    
        if res['code']=='0' :
            if res['success']:
                try:
                    msg(f"{res['data']['rewardMsg']}✅\n")
                except:
                    msg(f"{res['message']}\n")   
            else:
                msg(f"{res['message']}\n")
        else:
            msg('错误⭕')
            msg(f'{res}\n')


# 主页面任务领取能量
def page_task(cookie,assignmentId,projectId,title,itemId):
    msg(f'开始 {title}📑')
    body={"projectId":projectId,"assignmentId":assignmentId,"type":"1","itemId":itemId}
    res=taskPostUrl_4("interactive_done", body, cookie)
    if not res:
        return    
    if res['code']=='0' :
        if res['success']:
            try:
                msg(f"{res['data']['rewardMsg']}✅\n")
            except:
                msg(f"{res['message']}\n")  
        else:
            msg(f"{res['message']}\n")
    else:
        msg('错误⭕')
        msg(f'{res}\n')


# 主页面任务id
def page_taskid(cookie,assignmentId,projectId):
    body={"type":"1","projectId":projectId,"assignmentId":assignmentId,"doneHide":False}
    msg('获取主页面任务id🔎...')
    res=taskPostUrl_3("interactive_info", body, cookie)
    if not res:
        return    
    if res['code']=='0':
        if res['success']:
            try:
                title=res['data'][0]['title']
                itemId=res['data'][0]['itemId']
                return [title,itemId]
            except:
                msg(f"没有找到任务id\n")    
        else:
            msg(f"没有找到任务id\n") 
    else:
        msg('错误⭕')
        msg(f'{res}\n')    


# 获取邀请码
def get_inviteId(cookie,assignmentId,projectId):
    global inviteId_list
    body={"type":"2","projectId":projectId,"assignmentId":assignmentId,"doneHide":False,"helpType":"1","itemId":""}
    msg('获取邀请码🔎..')
    res=taskPostUrl_3("interactive_info", body, cookie)
    if not res:
        return    
    if res['code']=='0' :
        if res['success']:
            try:
                # print(res)
                inviteId=res['data'][0]['itemId']
                if inviteId not in inviteId_list:
                    inviteId_list.append(inviteId)
                    msg(f"账号{get_pin(cookie)}的邀请码是 {inviteId}✅\n")
                else:
                    msg(f"已记录过该邀请码\n")
            except:
                msg(f"没有找到邀请码\n")  
        else:
            msg(f"没有找到邀请码\n")
    else:
        msg('错误')
        msg(f'{res}\n') 


# 助力
def boost(cookie,assignmentId,projectId,inviteId):
    body={"type":"2","projectId":projectId,"assignmentId":assignmentId,"doneHide":False,"helpType":"2","itemId":inviteId}
    res=taskPostUrl_3("interactive_info", body, cookie)
    if not res:
        return    
    if res['code']=='0' :
        if res['success']:
            try:
                # print(res['data'])
                a=res['data'][0]['msg']
                msg(f'账号{get_pin(cookie)}去助力{inviteId}📑...')
                msg(f"{a}\n")
            except:
                pass
                # msg(f"{res['message']}\n")  
        else:
            pass
            # msg(f"{res['message']}\n")
    else:
        msg('错误')
        msg(f'{res}\n') 



# 获取所有任务数据，分配任务
def task_id(cookie):
    # 数据源1
    url='https://prodev.m.jd.com/mall/active/qyteDVYBqzar2x6S9rcsBYQJXhW/index.html?_ts=1635062092818&utm_source=iosapp&utm_medium=appshare&utm_campaign=t_335139774&utm_term=Qqfriends&ad_od=share&utm_user=plusmember&gx=RnFikG5YbzSPntRf7Nl_WBPsc0vAzg&tttparams=NRuRseyJnTGF0IjoiMzAuMjczNzIiLCJnTG5nIjoiMTA3LjY0ODcxMi5J9&sid=683bb76d3f8c68afb54a6699eb4a030w&un_area=4_134_19915_0'
    headers={
        'Cookie': cookie,
        'Host': 'prodev.m.jd.com',
        'Connection': 'keep-alive',
        'Content-Type': 'application/x-www-form-urlencoded',
        "User-Agent": ua(),
        'Accept-Language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7',
        'Accept-Encoding': 'gzip, deflate, br',
    }
    for n in range(3):
        try:
            res = requests.get(url=url, headers=headers, timeout=10,verify=False)
            res.encoding='utf-8'
            res=res.text
        except:
            if n==3:
                msg('API请求失败，请检查网路重试❗\n')
                return 

    # 数据源2
    url_2='https://api.m.jd.com/?client=wh5&clientVersion=1.0.0&functionId=qryH5BabelFloors'
    headers_2={
        'Cookie': cookie,
        'Host': 'api.m.jd.com',
        'Connection': 'keep-alive',
        'Content-Type': 'application/x-www-form-urlencoded',
        "User-Agent": ua(),
        'Accept-Language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7',
        'Accept-Encoding': 'gzip, deflate, br',  
    }
    body_2={"activityId":"qyteDVYBqzar2x6S9rcsBYQJXhW","paginationParam":"2","paginationFlrs":"[[65545401,65545402,65545403,65690186,65633233,65751866,65545406,65578502,65545407,65578503,65735501,65578504,65545408],[65735500,65545409,65690061,65545410,65690062,65545411,65956790,65956791,65956792,65545413,65545412,65545415,65545416,66027650,66027651,66027652,66027653]]"}
    data_2=f'body={json.dumps(body_2)}&sid=683bb76d3f8c68afb54a6699eb4a030w&uuid=8363031323830343433313332303-13d2438366461633039353566366&area=4_134_19915_0&osVersion=9'
    for n in range(3):
        try:
            res_2 = requests.post(url=url_2, headers=headers_2,data=data_2, timeout=10,verify=False)
            res_2.encoding='utf-8'
            res_2=res_2.text
        except:
            if n==3:
                msg('API请求失败，请检查网路重试❗\n')
                return 

    global taskCode_list,projectId_list
    try:
        # 处理数据1
        advId1=re.findall(r'"advId1":\[(.+?)\]',res,re.M)
        advId2=re.findall(r'"advId2":\[(.+?)\]',res,re.M)
        assignmentId_list=re.findall(r'"assignmentid":"(.+?)"',res,re.M)
        projectId_list=re.findall(r'"programid":"(.+?)"',res,re.M)
        advId1_advGrpId=[re.findall(r'"advGrpId":"(.+?)"',advId)[0] for advId in advId1]
        advId2_advGrpId=[re.findall(r'"advGrpId":"(.+?)"',advId)[0] for advId in advId2]
        taskCode_list=re.findall(r'"taskCode":"(.+?)"',res,re.M)

        # 处理数据2
        advId1_2=re.findall(r'"advId1":\[(.+?)\]',res_2,re.M)
        advId2_2=re.findall(r'"advId2":\[(.+?)\]',res_2,re.M)
        assignmentId_list_2=re.findall(r'"assignmentid":"(.+?)"',res_2,re.M)
        projectId_list_2=re.findall(r'"programid":"(.+?)"',res_2,re.M)
        advId1_advGrpId_2=[re.findall(r'"advGrpId":"(.+?)"',advId)[0] for advId in advId1_2]
        advId2_advGrpId_2=[re.findall(r'"advGrpId":"(.+?)"',advId)[0] for advId in advId2_2]
        taskCode_list_2=re.findall(r'"taskCode":"(.+?)"',res_2,re.M)

        # 整理数据
        assignmentId_list+=assignmentId_list_2
        projectId_list+=projectId_list_2
        advId1_advGrpId+=advId1_advGrpId_2
        advId2_advGrpId+=advId2_advGrpId_2
        taskCode_list+=taskCode_list_2
        assignmentId_list=set(assignmentId_list)
        projectId_list=set(projectId_list)
        advId1_advGrpId=set(advId1_advGrpId)
        advId2_advGrpId=set(advId2_advGrpId)
        taskCode_list=set(taskCode_list)
    except:
        msg(f'收集任务数据失败，快去买买买吧\n')
        return

    # print(assignmentId_list)
    # print(projectId_list)
    # print(advId1_advGrpId)
    # print(advId2_advGrpId)

    # 遍历数据
    for assignmentId in assignmentId_list:
        for e,projectId in enumerate(projectId_list):
            for f,taskCode in enumerate(taskCode_list):
                taskid=page_taskid(cookie,taskCode,projectId)          # 主页面任务id
                if taskid:
                    page_task(cookie,taskCode,projectId,taskid[0],taskid[1])          # 主页面任务
                get_inviteId(cookie,taskCode,projectId)                # 获取邀请码
            for advGrpId1 in advId1_advGrpId:
                for advGrpId2 in advId2_advGrpId:
                    pass
                    skuList=task_assignment(cookie,assignmentId,projectId,advGrpId1,advGrpId2)        # 获取活动数据
                    if skuList:
                        time.sleep(0.5)
                        skuList_task(cookie,skuList[0],skuList[1],skuList[2])        # 分配子任务
    

def main():
    msg('🔔发现新宝藏，开始！\n')
    global inviteId_list
    inviteId_list=[]
    msg(f'====================共{len(cookie_list)}京东个账号Cookie=========\n')

    for e,cookie in enumerate(cookie_list,start=1):
        msg(f'******开始【账号 {e}】 {get_pin(cookie)} *********\n')
        if not getUserInfo(cookie):
            continue
        task_id(cookie)

    msg(f'\n\n====================开始内部助力=========\n')

    for f,inviteId in enumerate(inviteId_list,start=1):
        for e,cookie in enumerate(cookie_list,start=1):
            try:
                for assignmentId in taskCode_list:
                   for projectId in projectId_list: 
                        boost(cookie,assignmentId,projectId,inviteId)
            except:
                msg('黑号吧\n')


    if run_send=='yes':
        send('### 发现新宝藏 ###')   # 通知服务


if __name__ == '__main__':
    main()

