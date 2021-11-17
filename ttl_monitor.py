import requests, json, os
gift_list = ['61', '62', '631', '633']


def gift_count(n):
    url = f'https://www.ttljf.com/ttl_site/giftApi.do?giftId={n}&mthd=giftDetail&sign=1275eded3f5a2ddc5794d59d97e0a852&userId=939777'
    result = requests.get(url).text
    r = json.loads(result)
    count = r['gifts']['giftCount']
    name = r['gifts']['giftName']
    return f'{name}当前数量：{count}\n'


def main():
    global n
    n = ''
    for i in gift_list:
        count,name = gift_count(i)
        s=f'{name}当前数量：{count}\n'
        if count!=0:
            pushplus_bot('太太乐',f'太太乐奖品兑换：\n{s}')
        else:
            print(f'太太乐奖品兑换：\n{s}')


# 定义pushplus推送
def pushplus_bot(title, content):
    PUSH_PLUS_TOKEN = os.environ['PUSH_PLUS_TOKEN']
    try:
        print("\n")
        if not PUSH_PLUS_TOKEN:
            print("PUSHPLUS服务的token未设置!!\n取消推送")
            return
        print("PUSHPLUS服务启动")
        url = 'http://www.pushplus.plus/send'
        data = {
            "token": PUSH_PLUS_TOKEN,
            "title": title,
            "content": content
        }
        body = json.dumps(data).encode(encoding='utf-8')
        headers = {'Content-Type': 'application/json'}
        response = requests.post(url=url, data=body, headers=headers).json()
        if response['code'] == 200:
            print('推送成功！')
        else:
            print('推送失败！')
    except Exception as e:
        print(e)


if __name__ == '__main__':
    main()
