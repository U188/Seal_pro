import requests
import re
import json,time
requests.packages.urllib3.disable_warnings()
cookies='pt_key=app_openAAJh1jJLADCnGz9LgUs_S7pznxktTczn87ZxP5D3A9rDC2J0owDPjzIZ3fetfxI1SOXrj7VyVvM;pt_pin=jd_6cbdcc9521870;'

headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36'
    }
def getinfo():
    info_list=[]
    url='https://www.qitoqito.com/beans/'
    resp = requests.get(url=url,headers=headers,verify=False).text
    info = re.compile(r"href=(.+?) timestamp").findall(resp)
    for i in info:       
        shopid=re.compile(r'shopid=(.+?)venderid').findall(i)[0].replace('\"',"").replace(' ',"")
        venderid=re.compile(r'venderid=(.+?)activityid').findall(i)[0].replace('\"',"").replace(' ',"")
        activityid=re.compile(r'activityid=(.+?)name').findall(i)[0].replace('\"',"").replace(' ',"")
        name=re.compile(r'name=\"(.+?)\"').findall(i)[0].replace('\"',"").replace(' ',"")
        m={"shopid":shopid,"venderid":venderid,"activityid":activityid,"name":name}
        info_list.append(m)
    return info_list
# 获取pin
cookie_findall=re.compile(r'pt_pin=(.+?);')
def get_pin(cookie):
    try:
        return cookie_findall.findall(cookie)[0]
    except:
        print('ck格式不正确，请检查')
def write_text(text):
    with open('./shopGift.txt','a') as f:
        f.write(text)
def read_text():
    with open('./shopGift.txt','r') as f:
        f=f.read()
    return f
def ShopGift():
    cookies_list=cookies.split('#')
    info_list=getinfo()
    for cookie in cookies_list:
        for info in info_list:
            #print(info)
            shopId=info['shopid']
            venderId=info['venderid']
            activityId=info['activityid']
            name=info['name']
            infoo=f'"shopid":{shopId},"venderid":{venderId},"activityid":{activityId}\n'
            read=read_text()
            if infoo in read:
                print(f'{name}已经领取了')
                #time.sleep(30)
            else:
                #print(shopId,venderId,activityId)
                if len(activityId)>0:
                    pinName=get_pin(cookie)
                    body='functionId=drawShopGift&body={"follow":0,"shopId":"'+shopId+'","activityId":"'+activityId+'","sourceRpc":"shop_app_home_window","venderId":"'+venderId+'"}&client=apple&clientVersion=10.0.4&osVersion=13.7&appid=wh5&loginType=2&loginWQBiz=interact'
                    result=taskpost(body,cookie,infoo)
                    getGiftresult(result,pinName)
                    #time.sleep(600)
                else:
                    print(f'{name}店铺没有奖励')

def memoryFun(pinName,bean):
    global usergetGiftinfo
    try:
        try:

            usergetGiftinfo['{}'.format(pinName)]
            usergetGiftinfo['{}'.format(pinName)] += bean
        except:
            usergetGiftinfo['{}'.format(pinName)] = bean
    except Exception as e:
        print(e)

def getGiftresult(result,pinName):
    try:
        if result['isSuccess']:
            if result['result']:
                followDesc = result['result']['followDesc']
                giftDesc = result['result']['giftDesc']
                print(f"\t└账号【{pinName}】{followDesc}>{giftDesc}")
                if result['result']['giftCode'] == '200':
                    try:
                        alreadyReceivedGifts = result['result']['alreadyReceivedGifts']
                        
                        for g in alreadyReceivedGifts:
                            if g['prizeType'] == 4:
                                bean = g['redWord']
                                memoryFun(pinName, int(bean))
                            print(f"\t\t└获得{g['rearWord']}:{g['redWord']}")
                    except:
                        pass
        else:
            print()
    except Exception as e:
        print(f"getGiftresult Error {e}")


def taskpost(body,cookie,infoo):
    headers = {
            'J-E-H' : '%7B%22ciphertype%22:5,%22cipher%22:%7B%22User-Agent%22:%22IuG0aVLeb25vBzO2Dzq2CyUyCMrfUQrlbwU7TJSmaU9JTJSmCJCkDzivCtLJY2PiZI8yBtKmAG==%22%7D,%22ts%22:1636156765,%22hdid%22:%22JM9F1ywUPwflvMIpYPok0tt5k9kW4ArJEU3lfLhxBqw=%22,%22version%22:%221.0.3%22,%22appname%22:%22com.360buy.jdmobile%22,%22ridx%22:-1%7D',
            'Accept-Encoding': 'gzip, deflate, br',
            'Cookie': cookie,
            'Connection': 'close',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Accept': '*/*',
            'Host': 'api.m.jd.com',
            'User-Agent': 'JD4iPhone/167685 (iPhone; iOS 14.3; Scale/3.00)',
            'Referer': '',
            'J-E-C' : '%7B%22ciphertype%22:5,%22cipher%22:%7B%22pin%22:%22TUU5TJuyTJvQTUU3TUOnTJu1TUU1TUSmTUSnTUU2TJu4TUPQTUU0TUS4TJrOTUU1TUSmTJq2TUU1TUSmTUSn%22%7D,%22ts%22:1636157606,%22hdid%22:%22JM9F1ywUPwflvMIpYPok0tt5k9kW4ArJEU3lfLhxBqw=%22,%22version%22:%221.0.3%22,%22appname%22:%22com.360buy.jdmobile%22,%22ridx%22:-1%7D',
            'Accept-Language': 'zh-Hans-CN;q=1'
        }
    try:
        url = 'https://api.m.jd.com/client.action?g_ty=ls&g_tk=518274330'
        response = requests.post(url, headers=headers, verify=False, data=body, timeout=60)
        if 'isSuccess' in response.text:
                write_text(infoo)
                return response.json()
        else:
            return 9
    except Exception as e:
        print(e)
        return 9


if __name__ == '__main__':
    ShopGift()
