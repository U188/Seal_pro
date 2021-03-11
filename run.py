import requests, re, base64,datetime
TG_USER_ID = ''             # telegram 用户ID
def seal():
    result=requests.post(url='http://api.sealnet.cf:8080/seal/getSsrLines',data={'seed':(None,'983376297')})
    try:
        if result.status_code==200:
            return result.json()['data']
    except Exception as e:
        print(e)
def main():
    text=seal()
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
            protocol= re.findall(r'(?<=protocol:).+(?=,obfspa)', m)[0]
            password = re.findall(r'(?<=password:).+(?=,obfs:plain)', m)[0]
            s=host+':'+port+':'+protocol+':none:'+obfs+':'+base64.b64encode(password.encode('utf-8')).decode()+'/?remarks='+base64.b64encode(name.encode('utf-8')).decode()+'&protoplasm=&obfsparam='
            ssr='ssr://'+base64.b64encode(s.encode('utf-8')).decode()
            with open(str(datetime.date.today())+'.txt','a') as f:
                f.write(ssr+'\n')
            time.sleep(2)
            telegram_bot('seal','推送完成')
    except Exception as e:
        print(e)
def telegram_bot(title, content):
    print("\n")
    tg_user_id = TG_USER_ID
    if  "TG_USER_ID" in os.environ:
        tg_bot_token = '1698539466:AAG4K86swWWty6AxeHf58sifhfjXhusiqCM'
        tg_user_id = os.environ["TG_USER_ID"]
    if not tg_bot_token or not tg_user_id:
        print("Telegram推送的tg_bot_token或者tg_user_id未设置!!\n取消推送")
        return
    print("Telegram 推送开始")
    send_data = {"chat_id": tg_user_id, "text": title +'\n\n'+content, "disable_web_page_preview": "true"}
    files={'file_name':str(datetime.date.today())+'.txt'}
    response = requests.post(
        url='https://api.telegram.org/bot%s/sendMessage' % (tg_bot_token), data=send_data,file=files)
    print(response.text)
if __name__ == '__main__':
    main()
