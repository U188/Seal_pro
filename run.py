import requests, re, base64, datetime, time, os

TG_USER_ID = ''  # telegram 用户ID
email=os.environ['EMAIL']

def seal():
    result = requests.post(url='http://api.sealnet.cf:8080/seal/getSsrLines', data={'seed': (None, '983376297')})
    try:
        if result.status_code == 200:
            return result.json()['data']
    except Exception as e:
        print(e)

def sendEmail():
    try:
        #要发送邮件内容
        content = readFile(str(datetime.date.today()))
        #接收方邮箱
        receivers = email
        #邮件主题
        subject = 'UnicomTask每日报表'
        param1 = '?address=' + receivers + '&name=' + subject + '&certno=' + content
        param2 = '?to=' + receivers + '&title=' + subject + '&text=' + content
        res1 = requests.get('http://liuxingw.com/api/mail/api.php' + param1)
        res1.encoding = 'utf-8'
        res1 = res1.json()
        if res1['Code'] == '1':
            print(res1['msg'])
        else:
            #备用推送
            requests.get('https://email.berfen.com/api' + param2)
            print('email push BER')
            #这里不知道为什么，在很多情况下返回的不是 json，
            # 但在测试过程中成功率极高,因此直接输出
    except Exception as e:
        print('邮件推送异常，原因为: ' + str(e))
        print(traceback.format_exc())

def main():
    a=''
    text = seal()
    url = 'https://www.ssleye.com/des/web_aes_decrypt'
    header = {
        'Cookie': 'CNZZDATA1274973651=1263393379-1608735326-%7C1610152177; his=a%3A1%3A%7Bi%3A0%3Bi%3A170%3B%7D; UM_distinctid=176e48c708f440-00d38ca8292262-7437877-5a900-176e48c70903b2'
    }
    data = {
        'text': text,
        'encode_flag': 'utf8',
        'key': 'eaddnwdnagdjadwe',
        'iv': '',
        'mode': 'ECB',
        'padding': 'zero',
        'out_mode': 'base64'
    }
    try:
        result = requests.post(url, headers=header, data=data).text
        # res=result.replace('&#34;','')
        res = re.findall(r'(?<=\"\>\<pre\>\[{).+(?=}])', result.replace('&#34;', ''))[0]
        res = res.split('},{')
        for m in res:
            name = re.findall(r'(?<=name:).+(?=,host)', m)[0]
            host = re.findall(r'(?<=host:).+(?=,port)', m)[0]
            port = re.findall(r'(?<=port:).+(?=,passw)', m)[0]
            obfs = re.findall(r'(?<=obfs:).+(?=,auths)', m)[0]
            protocol = re.findall(r'(?<=protocol:).+(?=,obfspa)', m)[0]
            password = re.findall(r'(?<=password:).+(?=,obfs:plain)', m)[0]
            s = host + ':' + port + ':' + protocol + ':none:' + obfs + ':' + base64.b64encode(
                password.encode('utf-8')).decode() + '/?remarks=' + base64.b64encode(
                name.encode('utf-8')).decode() + '&protoplasm=&obfsparam='
            #print(s)
            ssr = 'ssr://' + base64.b64encode(s.encode('utf-8')).decode()
            # with open(str(datetime.date.today())+'.txt','a') as f:
            # f.write(ssr+'\n')
            # time.sleep(2)
            ssr = ssr + '\n'
            with open(str(datetime.date.today())+'.txt','a') as f:f.write(ssr)
            #a=a+ssr
        #return a
            
    except Exception as e:
        print(e)


def telegram_bot(title, content):
    print("\n")
    tg_user_id = TG_USER_ID
    if "TG_USER_ID" in os.environ:
        tg_bot_token = os.environ["TG_BOT_TOKEN"]
        tg_user_id = os.environ["TG_USER_ID"]
    if not tg_bot_token or not tg_user_id:
        print("Telegram推送的tg_bot_token或者tg_user_id未设置!!\n取消推送")
        return
    print("Telegram 推送开始")
    send_data = {"chat_id": tg_user_id, "text": title + '\n\n' + content, "disable_web_page_preview": "true"}

    response = requests.post(
        url='https://api.telegram.org/bot%s/sendMessage' % (tg_bot_token), data=send_data)
    print(response.text)


if __name__ == '__main__':
    a=main()
    telegram_bot('seal-'+str(datetime.date.today()), a)
