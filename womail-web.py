# -*- coding: utf-8 -*-
import requests
import json
import re
import os
import sys
import time
import hashlib
from urllib import parse

#账号配置
# 脚本内填写 ,按自然数顺序填写，最多999条
womail_url_1=""
womail_account_1="手机号@wo.cn"
womail_password_1=""

womail_url_2=""
womail_account_2="手机号@wo.cn"
womail_password_2=""

# womail_url_n=""       
# womail_account_n="手机号@wo.cn"
# womail_password_n=""  

'''
# 环境变量填写 ,会优先读取环境变量,按自然数顺序填写，最多999条
export womail_url_1=""
export womail_account_1="手机号@wo.cn"
export womail_password_1=""

export womail_url_2=""
export womail_account_2="手机号@wo.cn"
export womail_password_2=""

export womail_url_n=""       
export womail_account_n="手机号@wo.cn"
export womail_password_n=""  
'''

# 读取不固定环境变量,返回的是list
def get_env_nofixed(env):
    a=[]
    for n in range(1,999):
        try:
            if f'{env}_1' in os.environ:
                b=os.environ[f'{env}_{n}']
            elif '/jd' in os.path.abspath(os.path.dirname(__file__)):
                b=v4_env(f'{env}_{n}')
            else:
                b=eval(f'{env}_{n}')
            a.append(b)
        except:
            break
    return a

# v4
def v4_env(env):
    b=re.compile(r'(?:export )?'+env+r' ?= ?[\"\'](.*?)[\"\']', re.I)
    with open('/jd/config/config.sh', 'r') as f:
        for line in f.readlines():
            try:
                c=b.match(line).group(1)
                break
            except:
                pass
    return c 


## 获取通知服务
class Msg(object):
    def getsendNotify(self, a=1):
        try:
            url = 'https://ghproxy.com/https://raw.githubusercontent.com/wuye999/myScripts/main/sendNotify.py'
            response = requests.get(url)
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
        cur_path = os.path.abspath('.')
        sys.path.append(cur_path)
        for n in range(3):
            if os.path.exists(cur_path + "/sendNotify.py"):
                try:
                    from sendNotify import send,msg,initialize
                    break
                except:
                    self.getsendNotify()
            else:
                self.getsendNotify()
        l=['BARK','PUSH_KEY','TG_BOT_TOKEN','TG_USER_ID','TG_API_HOST','TG_PROXY_HOST','TG_PROXY_PORT','DD_BOT_TOKEN','DD_BOT_SECRET','QQ_SKEY','Q_SKEY','QQ_MODE','QYWX_AM','PUSH_PLUS_TOKEN']
        d={}
        for a in l:
            try:
                d[a]=eval(a)
            except:
                d[a]=''
        initialize(d)   # 初始化        
Msg().main()   # 初始化通知服务 



#最大连续签到天数,如果设置为21则表示签到21天后,断签一天
max_sign_days=21
UA='"User-Agent: Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.25 Safari/537.36 Core/1.70.3868.400 QQBrowser/10.8.4394.400"'
def do_task_1(womail_url):
    #登录获取Cookie
    if womail_url == '':
        msg('未配置沃邮箱账号')
        return 1
    try:
        url = womail_url
        headers = {
            "User-Agent": UA
        }
        res = requests.get(url=url, headers=headers, allow_redirects=False)
        set_cookie = res.headers["Set-Cookie"]
        cookies = re.findall("YZKF_SESSION.*?;", set_cookie)[0]
        if "YZKF_SESSION" in cookies:
            msg('获取cookie成功')
        else:
            msg('沃邮箱获取 cookies 失败')
            return None
    except Exception as e:
        msg('沃邮箱错误:')
        msg(e)
        return None
    headers = {
        "User-Agent": UA,
        "Cookie": cookies,
    }
    #查询签到天数
    try:
        url = "https://nyan.mail.wo.cn/cn/sign/index/userinfo.do?rand=0.2967650751258384"
        response = requests.post(url=url, headers=headers)
        keepSign=json.loads(response.text).get('result').get('keepSign')
        msg('已连续签到'+str(keepSign)+'天')
        if keepSign >= max_sign_days:
            msg('连续签到天数大于设定次数,暂停签到')
        else:
            #执行签到任务
            try:
                url = "https://nyan.mail.wo.cn/cn/sign/user/checkin.do?rand=0.913524814493383"
                response = requests.post(url=url, headers=headers)
                result=json.loads(response.text).get('result')
                if result == -2:
                    msg('每日签到: 已签到')
                elif result is None:
                    msg('每日签到: 签到失败')
                else:
                    msg('每日签到: 签到成功,已签到'+str(result)+'天！')
            except Exception as e:
                msg('沃邮箱签到错误')
                msg(e)
    except Exception as e:
        msg('查询签到天数错误')
        msg(e)
    #执行其他任务
    try:
        url = "https://nyan.mail.wo.cn/cn/sign/user/doTask.do?rand=0.8776674762904109"
        data_params = {
            "邀请好友关注沃邮箱": {"taskName": "invite"},
            "每日首次登录手机邮箱": {"taskName": "loginmail"},
            "去用户俱乐部逛一逛": {"taskName": "club"},
            "小积分抽大奖": {"taskName": "clubactivity"},
        }
        for key, data in dict.items(data_params):
            try:
                response = requests.post(url=url, data=data, headers=headers)
                result=json.loads(response.text).get('result')
                if result == 1:
                    msg(str(key)+': 做任务成功')
                elif result == -1:
                    msg(str(key)+': 任务已做过')
                elif result == -2:
                    msg(str(key)+': 请检查登录状态')
                else:
                    msg(str(key)+': 未知错误')
            except Exception as e:
                msg('沃邮箱执行任务【''+str(key)+''】错误')
                msg(e)
    except Exception as e:
        msg('沃邮箱执行任务错误')
        msg(e)
        return None
    return 1

def do_task_2(womail_url):
    if womail_url == '':
        msg('未配置沃邮箱账号')
        return 1
    userdata = re.findall("mobile.*", womail_url)[0]
    url = "https://club.mail.wo.cn/clubwebservice/?" + userdata
    headers = {
        "User-Agent": UA
    }
    #获取俱乐部cookies
    try:
        res = requests.get(url=url, headers=headers, allow_redirects=False)
        set_cookie = res.headers["Set-Cookie"]
        cookies = re.findall("SESSION.*?;", set_cookie)[0]
        if "SESSION" in cookies:
            headers = {
                "User-Agent": UA,
                "Cookie": cookies,
                "Referer": "https://club.mail.wo.cn/clubwebservice/club-user/user-info/mine-task"
            }
        else:
            msg('登录俱乐部错误')
            return None
        #查询签到天数
        try:
            url = "https://club.mail.wo.cn/clubwebservice/club-user/user-sign/query-continuous-sign-record"
            response = requests.get(url=url, headers=headers)
            newContinuousDay=json.loads(response.text)[0].get('newContinuousDay')
            msg('已连续签到'+str(newContinuousDay)+'天')
            if newContinuousDay >= max_sign_days:
                msg('连续签到天数大于设定次数,暂停签到')
            else:
                #任务签到
                url = 'https://club.mail.wo.cn/clubwebservice/club-user/user-sign/create?channelId='
                response = requests.get(url=url,headers=headers)
                description=json.loads(response.text).get('description')
                msg('成长值签到结果:'+str(description))
        except Exception as e:
            msg('查询签到天数错误')
            msg(e)
        #积分任务
        url = 'https://club.mail.wo.cn/clubwebservice/growth/queryIntegralTask'
        response = requests.get(url=url,headers=headers)
        datas=json.loads(response.text).get('data')
        for data in datas:
            if data['irid'] == None or data['irid'] == 339 or data['taskState'] == 1:
                msg('跳过'+str(data['resourceName']))
                continue
            url = 'https://club.mail.wo.cn/clubwebservice/growth/addIntegral?resourceType='+parse.quote(str(data['resourceFlag']))
            response = requests.get(url=url,headers=headers)
            description=json.loads(response.text).get('description')
            msg('执行任务:'+str(data['resourceName'])+'状态:'+str(description))
        #成长值任务
        url = 'https://club.mail.wo.cn/clubwebservice/growth/queryGrowthTask'
        response = requests.get(url=url,headers=headers)
        datas=json.loads(response.text).get('data')
        for data in datas:
            if data['irid'] == None or data['irid'] == 576 or data['taskState'] == 1:
                msg('跳过'+str(data['resourceName']))
                continue
            url = 'https://club.mail.wo.cn/clubwebservice/growth/addGrowthViaTask?resourceType='+parse.quote(str(data['resourceFlag']))
            response = requests.get(url=url,headers=headers)
            description=json.loads(response.text).get('description')
            msg('执行任务:'+str(data['resourceName'])+'状态:'+str(description))
    except Exception as e:
        msg('登录俱乐部错误:')
        msg(e)
        return None
    return 1

def do_wo_email_task(uid,password):
    #登录获取Cookie
    if uid == '' or password == '':
        msg('未配置沃邮箱账号')
        return 1
    try:
        url = 'https://mail.wo.cn/coremail/s/json?func=user:login'
        headers = {
            "User-Agent": 'okhttp/${project.version}'
        }
        data_json = {"uid": ""+str(uid)+"", "password": ""+str(password)+""}
        response = requests.post(url=url,headers=headers,data=json.dumps(data_json))
        code=json.loads(response.text).get('code')
        msg('登录沃邮箱结果:'+str(code))
        sid=re.findall('"sid":"(.*?)"',response.text)[0]
        set_cookie = response.headers["Set-Cookie"]
        cookie = re.findall("Coremail.*?;", set_cookie)[0]
        cookie=cookie+'Coremail.sid='+str(sid)+';'
        if "Coremail" not in cookie:
            msg('沃邮箱获取 sid,Coremail 失败')
            return None
        #app
        cookies=cookie+'domain=mail.wo.cn;'
        headers = {
            "User-Agent": UA,
            "Cookie": cookies,
            "Accept": "text/x-json",
            "Content-Type": "text/x-json",
            "X-CM-SERVICE": "PHONE",
            "Origin": "https://mail.wo.cn",
            "X-Requested-With": "com.asiainfo.android",
            "Sec-Fetch-Site": "same-origin",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Dest": "empty"
        }
        #增加积分
        integral_data = {
            "每日登录": 'login',
            "发送邮件": 'sendMail',
            "查看邮件": 'listMail',
            "登录百度网盘": 'baiduCloud',
            "新建日程": 'createCal',
        }
        for key, userAction in dict.items(integral_data):
            try:
                url = 'https://mail.wo.cn/coremail/s/?func=club:addClubInfo&sid='+str(sid)
                data_json = {"uid": ""+str(uid)+"","userAction":""+str(userAction)+"","userType":"integral"}
                response = requests.post(url=url,headers=headers,data=json.dumps(data_json))
                code=json.loads(response.text).get('code')
                msg(key+'app积分结果:'+str(code))
            except Exception as e:
                msg('app沃邮箱执行任务错误:')
                msg(e)
                return None
        #增加成长值
        growth_data = {
            "每日登录": 'login',
            "发送邮件": 'sendMail',
            "查看邮件": 'listMail',
            "登录百度网盘": 'baiduCloud',
            "新建日程": 'createCal',
        }
        for key, userAction in dict.items(integral_data):
            try:
                url = 'https://mail.wo.cn/coremail/s/?func=club:addClubInfo&sid='+str(sid)
                data_json = {"uid": ""+str(uid)+"","userAction":""+str(userAction)+"","userType":"growth"}
                response = requests.post(url=url,headers=headers,data=json.dumps(data_json))
                code=json.loads(response.text).get('code')
                msg(key+'app成长值结果:'+str(code))
            except Exception as e:
                msg('app沃邮箱执行任务错误:')
                msg(e)
                return None
            
        #网页
        cookies=cookie+'CoremailReferer=https%3A%2F%2Fmail.wo.cn%2Fcoremail%2Fhxphone%2F;'
        headers = {
            "User-Agent": UA,
            "Cookie": cookies,
            "Accept": "text/x-json",
            "Content-Type": "text/x-json",
            "Origin": "https://mail.wo.cn",
            "X-Requested-With": "com.tencent.mm",
            "Sec-Fetch-Site": "same-origin",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Dest": "empty"
        }
        #增加积分
        integral_data = {
            "每日登录": 'login',
            "发送邮件": 'sendMail',
            "查看邮件": 'listMail',
            "登录百度网盘": 'baiduCloud',
            "新建日程": 'createCal',
            "上传文件到中转站": 'uploadFile',
        }
        for key, userAction in dict.items(integral_data):
            try:
                url = 'https://mail.wo.cn/coremail/s/?func=club:addClubInfo&sid='+str(sid)
                data_json = {"uid": ""+str(uid)+"","userAction":""+str(userAction)+"","userType":"integral"}
                response = requests.post(url=url,headers=headers,data=json.dumps(data_json))
                code=json.loads(response.text).get('code')
                msg(key+'网页端积分结果:'+str(code))
            except Exception as e:
                msg('网页端沃邮箱执行任务错误:')
                msg(e)
                return None
        #增加成长值
        growth_data = {
            "每日登录": 'login',
            "发送邮件": 'sendMail',
            "查看邮件": 'listMail',
            "登录百度网盘": 'baiduCloud',
            "新建日程": 'createCal',
            "上传文件到中转站": 'uploadFile',
        }
        for key, userAction in dict.items(integral_data):
            try:
                url = 'https://mail.wo.cn/coremail/s/?func=club:addClubInfo&sid='+str(sid)
                data_json = {"uid": ""+str(uid)+"","userAction":""+str(userAction)+"","userType":"growth"}
                response = requests.post(url=url,headers=headers,data=json.dumps(data_json))
                code=json.loads(response.text).get('code')
                msg(key+'网页端成长值结果:'+str(code))
            except Exception as e:
                msg('网页端沃邮箱执行任务错误:')
                msg(e)
                return None
        
        #电脑
        cookies=cookie+'domain=;CoremailReferer=https%3A%2F%2Fmail.wo.cn%2Fcoremail%2Findex.jsp%3Fcus%3D1;'
        headers = {
            "User-Agent": UA,
            "Cookie": cookies,
            "Accept": "text/x-json",
            "Content-Type": "text/x-json",
            "Origin": "https://mail.wo.cn",
            "X-Requested-With": "XMLHttpRequest",
            "Sec-Fetch-Site": "same-origin",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Dest": "empty"
        }
        #增加积分
        integral_data = {
            "每日登录": 'login',
            "发送邮件": 'sendMail',
            "查看邮件": 'listMail',
            "登录百度网盘": 'baiduCloud',
            "新建日程": 'createCal',
            "上传文件到中转站": 'uploadFile',
        }
        for key, userAction in dict.items(integral_data):
            try:
                url = 'https://mail.wo.cn/coremail/s/?func=club:addClubInfo&sid='+str(sid)
                data_json = {"userAction":""+str(userAction)+""}
                response = requests.post(url=url,headers=headers,data=json.dumps(data_json))
                code=json.loads(response.text).get('code')
                msg(key+'电脑端积分结果:'+str(code))
            except Exception as e:
                msg('电脑端沃邮箱执行任务错误:')
                msg(e)
                return None
        
    except Exception as e:
        msg('web沃邮箱错误:')
        msg(e)
        return None
    return 1

def main():
    msg(f'====================共{len(womail_url_list)}个沃邮箱账号=========\n')
    for e,womail_url in enumerate(womail_url_list):
        msg(f'******开始【账号 {e+1}】{ womail_account_list[e][:3]}****************** *********\n')
        do_task_1(womail_url)
        do_task_2(womail_url)
        do_wo_email_task(womail_account_list[e],womail_password_list[e])


if __name__ == '__main__':
    womail_url_list=get_env_nofixed('womail_url')
    womail_account_list=get_env_nofixed('womail_account')
    womail_password_list=get_env_nofixed('womail_password')
    main()
    send('### 沃邮箱 ###')   # 启用通知服务
