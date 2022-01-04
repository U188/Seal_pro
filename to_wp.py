#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os,json,random,time,re,string,functools,asyncio,hashlib,hmac
import sys
import requests
import aiohttp
from email.mime.text import MIMEText
from email.header import Header
import smtplib
requests.packages.urllib3.disable_warnings()


'''
cron: 59 59 21 * * *
export inbox="xxxxxxxx@qq.com"
export wskey_list_1="pin=xxx;wskey=xxx;"
export to_wp_url_1="https://api.m.jd.com/client.action?functionId=receiveNecklaceCoupon&xxxxxxxx"
export to_wp_data_1="body=%7B%22channel%22%3Axxxxxxxx"
export wskey_list_2="pin=***;wskey=***;"
export to_wp_url_2="https://api.m.jd.com/client.action?functionId=receiveNecklaceCoupon&********"
export to_wp_data_2="body=%7B%22channel%22%3Axxxxxxxx"
...
'''


def get_env(env):
    try:
        if env in os.environ: a=os.environ[env]
        elif '/ql' in os.path.abspath(os.path.dirname(__file__)):
            try: a=v4_env(env,'/ql/config/config.sh')
            except: a=eval(env)
        elif '/jd' in os.path.abspath(os.path.dirname(__file__)):
            try: a=v4_env(env,'/jd/config/config.sh')
            except: a=eval(env)
        else: a=eval(env)
    except: a=''
    return a

def v4_env(env,paths):
    b=re.compile(r'(?:export )?'+env+r' ?= ?[\"\'](.*?)[\"\']')
    with open(paths, 'r') as f:
        for line in f.readlines():
            try:
                c=b.match(line).group(1)
                break
            except: pass
    return c 
def get_env_nofixed(env):
    a=[]
    for n in range(1,999):
        b=get_env(f'{env}_{n}')
        if b: a.append(b)
        else: break
    return a


async def async_main():
    global session
    tasks=list()
    wskey_list=get_env_nofixed('wskey_list')
    url_list=get_env_nofixed('to_wp_url')
    data_list=get_env_nofixed("to_wp_data") 
    async with aiohttp.ClientSession() as session:
        for url,data,wskey in zip(url_list,data_list,wskey_list):
            for n in range(10):
                tasks.append(post_url(url,data,wskey,n))
        await asyncio.wait(tasks)


cookie_findall=re.compile(r'pin=(.+?);')
def get_pin(cookie):
    try: return cookie_findall.findall(cookie)[0]
    except: print('ck格式不正确，请检查')

async def post_url(url,data,wskey,n):
    await asyncio.sleep(0.1*n)
    headers={
        'Host': 'api.m.jd.com',
        'cookie': wskey,
        'charset': 'UTF-8',
        'accept-encoding': 'br,gzip,deflate',
        'user-agent': 'okhttp/3.12.1;jdmall;android;version/10.3.0;build/91795;',
        'cache-control': 'no-cache',
        'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
    }
    async with session.post(url, headers=headers, data=data) as res:
        res =await res.text(encoding="utf-8")
        print(res)
        print('\n')
        if '领券成功' in res:
            global content
            content+=f'账号 {get_pin(wskey)} 领券成功\n'
            

def sendmail(title, content):
    inbox=get_env('inbox')
    if not inbox or inbox=='xxxxxxxx@qq.com': 
        print('未配置收信箱')
        return
    mail_host="smtp.163.com"
    mail_user="kirisame_marisas@163.com"
    mail_pass="NKVLOJKWETGENOKY"
    sender = 'kirisame_marisas@163.com'
    receivers = [inbox]
    mail_msg='''
        <html><head>
            <meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
        </head><body>
            <div style="line-height:1.6;font-family:'雾雨魔理沙','雾雨魔理沙','sans-serif';"><br>'''+content.replace('\n','<br>')+'''<br></div>
            <div class="ne-quoted"> <a href="https://mail-online.nosdn.127.net/wzpmmc/90fda2a455c37350f9fa0e4f988027df.jpg"
                    display:block;background:#fff; max-width: 400px; _width: 400px;padding:15px 0 10px 0;text-decoration: none;
                    outline:none;-webkit-tap-highlight-color:transparent;-webkit-text-size-adjust:none
                    !important;text-size-adjust:none !important;">
                                  <table cellpadding="0"
                        style="width: 100%; max-width: 100%; table-layout: fixed; border-collapse: collapse;color: #9b9ea1;font-size: 14px;line-height:1.3;-webkit-text-size-adjust:none !important;text-size-adjust:none !important;">
                        <tbody
                            style="font-family: 'PingFang SC', 'Hiragino Sans GB','WenQuanYi Micro Hei', 'Microsoft Yahei', '4', verdana !important; word-wrap:break-word; word-break:break-all;-webkit-text-size-adjust:none !important;text-size-adjust:none !important;">
                            <tr><td width="38" style="padding:0; box-sizing: border-box; width: 38px;">
                                    <img width="38" height="38"
                                        style="vertical-align:middle; width: 38px; height: 38px; border-radius:50%;"
                                        src="https://mail-online.nosdn.127.net/wzpmmc/90fda2a455c37350f9fa0e4f988027df.jpg">
                                </td><td style="padding: 0 0 0 10px; color: #31353b;">
                                    <div
                                        style="font-size: 16px;font-weight:bold; width:100%; white-space: nowrap; overflow:hidden;text-overflow: ellipsis;">
                                        雾雨魔理沙</div>
                                    <div
                                        style="font-size: 14px;width:100%; margin-top: 3px; white-space: nowrap; overflow:hidden;text-overflow: ellipsis;">
                                        邮差</div></td></tr><tr width="100%" style="font-size: 14px !important; width: 100%;">
                                <td colspan="2" style="padding:10px 0 0 0; font-size:14px !important; width: 100%;">
                                    <div
                                        style="width: 100%;font-size: 14px !important;word-wrap:break-word;word-break:break-all;">
                                        kirisame_Marisa</div></td></tr></tbody></table></a><html><body></body> </html></div></body></html>
    '''
    message = MIMEText(mail_msg, 'html', 'utf-8')
    message['Subject'] = title
    message['From'] = "kirisame_marisas@163.com"
    message['To'] =  inbox

    try:
        smtpObj = smtplib.SMTP()
        smtpObj.connect(mail_host, 25)
        smtpObj.login(mail_user,mail_pass)
        smtpObj.sendmail(sender, receivers, message.as_string())
        print ("邮件发送成功")
    except smtplib.SMTPException as e:
        print ("Error: 无法发送邮件")
        print(e)


def time_YmdHMS():
    return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))

def main():
    global content
    content=''''''
    asyncio.run(async_main())
    if content:
        content+=f"{time_YmdHMS()}\n"
        sendmail('59-20 领取成功', content)

if __name__ == '__main__':
    main()
