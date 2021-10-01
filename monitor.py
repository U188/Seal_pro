from telethon import TelegramClient, events
import time, os, sys, datetime, requests, random, string, re, json, httpx, asyncio
from jsonpath import jsonpath
import importlib

importlib.reload(sys)
requests.packages.urllib3.disable_warnings()
ckss = ''
cks = ckss.split('&')
timestamp = int(round(time.time() * 1000))
today = datetime.datetime.now().strftime('%Y-%m-%d')
pwd = repr(os.getcwd()).replace("'", '')
record = 'yes'  # False|True 或 yes |no  是否记录符合条件的shopid，
openCardBean = 1  # 只入送豆数量大于此值
onlyRecord = 'no'  ##yes 或 no  yes:仅记录，不入会。
timesleep = 2  # 请求间隔
api_id = 3420052
api_hash = "ec130bf6eb5a4b0710e6e989cbb7dd28"


async def getUserInfo(ck, pinName):
    url = 'https://me-api.jd.com/user_new/info/GetJDUserInfoUnion?orgFlag=JD_PinGou_New&callSource=mainorder&channel=4&isHomewhite=0&sceneval=2&_={}&sceneval=2&g_login_type=1&callback=GetJDUserInfoUnion&g_ty=ls'.format(
        timestamp)
    headers = {'Cookie': ck,
               'Accept': '*/*',
               'Connection': 'keep-alive',
               'Referer': 'https://home.m.jd.com/myJd/home.action',
               'Accept-Encoding': 'gzip, deflate, br',
               'Host': 'me-api.jd.com',
               'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 14_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.2 Mobile/15E148 Safari/604.1',
               'Accept-Language': 'zh-cn'}
    try:
        # respp = requests.get(url=url, verify=False, headers=headers, timeout=30)
        async with httpx.AsyncClient(verify=False, headers=headers, timeout=30) as client:
            respp = await client.get(url=url)
        resp = respp.text
        r = re.compile('GetJDUserInfoUnion.*?\\((.*?)\\)')
        result = r.findall(resp)
        userInfo = json.loads(result[0])
        nickname = userInfo['data']['userInfo']['baseInfo']['nickname']
        return (ck, nickname)
    except Exception as e:
        print(e)
        print(f"用户【{pinName}】Cookie 已失效！请重新获取。")
        return (ck, False)


async def getVenderId(shopId, headers):
    """
	:param shopId:
	:param headers
	:return: venderId
	"""
    url = 'https://shop.m.jd.com/?shopId={0}'.format(shopId)
    # resp = requests.get(url=url, verify=False, headers=headers, timeout=30)
    async with httpx.AsyncClient(verify=False, headers=headers, timeout=30) as client:
        resp = await client.get(url=url)
    resulttext = resp.text
    # print(resulttext)
    r = re.compile("venderId: \\'(\\d+)\\'")
    venderId = r.findall(resulttext)
    return venderId[0]


def nowtime():
    return datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')


async def getShopOpenCardInfo(venderId, headers, shopid, userName):
    """
	:param venderId:
	:param headers:
	:return: activityId,getBean 或 返回 0:没豆 1:有豆已是会员 2:记录模式（不入会）
	"""
    num1 = string.digits
    v_num1 = ''.join(random.sample(['1', '2', '3', '4', '5', '6', '7', '8', '9'], 1)) + ''.join(
        random.sample(num1, 4))
    url = 'https://api.m.jd.com/client.action?appid=jd_shop_member&functionId=getShopOpenCardInfo&body=%7B%22venderId%22%3A%22{2}%22%2C%22channel%22%3A406%7D&client=H5&clientVersion=9.2.0&uuid=&jsonp=jsonp_{0}_{1}'.format(
        timestamp, v_num1, venderId)
    async with httpx.AsyncClient(verify=False, headers=headers, timeout=30) as client:
        resp = await client.get(url=url)
    # resp = requests.get(url=url, verify=False, headers=headers, timeout=30)
    time.sleep(timesleep)
    resulttxt = resp.text
    r = re.compile('jsonp_.*?\\((.*?)\\)\\;', re.M | re.S | re.I)
    result = r.findall(resulttxt)
    cardInfo = json.loads(result[0])
    venderCardName = cardInfo['result']['shopMemberCardInfo']['venderCardName']
    print(f"\t╰查询入会礼包【{venderCardName}】{shopid}")
    openCardStatus = cardInfo['result']['userInfo']['openCardStatus']
    interestsRuleList = cardInfo['result']['interestsRuleList']
    if interestsRuleList == None:
        print('\t\t╰Oh,该店礼包已被领光了~')
        return (0, 0)
    try:
        if len(interestsRuleList) > 0:
            for i in interestsRuleList:
                if '京豆' in i['prizeName']:
                    getBean = int(i['discountString'])
                    activityId = i['interestsInfo']['activityId']
                    context = '{0}'.format(shopid)

                    url = 'https://shopmember.m.jd.com/member/memberCloseAccount?venderId={}'.format(venderId)
                    context = '[{0}]:入会{2}豆，【{1}】销卡：{3}'.format(nowtime(), venderCardName, getBean, url)

                    if getBean >= openCardBean:
                        print(f"\t╰{venderCardName}:入会赠送【{getBean}豆】，可入会")
                        context = '{0}'.format(shopid)

                        if onlyRecord == True:
                            print('已开启仅记录，不入会。')
                            return (2, 2)
                        if openCardStatus == 1:
                            url = 'https://shopmember.m.jd.com/member/memberCloseAccount?venderId={}'.format(
                                venderId)
                            print('\t\t╰[账号：{0}]:您已经是本店会员，请注销会员卡24小时后再来~\n注销链接:{1}'.format(userName, url))
                            context = '[{3}]:入会{1}豆，{0}销卡：{2}'.format(venderCardName, getBean, url, nowtime())

                            return (1, 1)
                        return (activityId, getBean)
                    print(f"\t\t╰{venderCardName}:入会送【{getBean}】豆少于【{openCardBean}豆】,不入...")
                    if onlyRecord == True:
                        print('已开启仅记录，不入会。')
                        return (2, 2)
                    return (
                        0, openCardStatus)
                    continue

            print('\t\t╰Oh~ 该店入会京豆已被领光了')
            return (0, 0)
        return (0, 0)
    except Exception as e:
        try:
            print(e)
        finally:
            e = None
            del e


async def bindWithVender(venderId, shopId, activityId, channel, headers):
    """
	:param venderId:
	:param shopId:
	:param activityId:
	:param channel:
	:param headers:
	:return: result : 开卡结果
	"""
    num = string.ascii_letters + string.digits
    v_name = ''.join(random.sample(num, 10))
    num1 = string.digits
    v_num1 = ''.join(random.sample(['1', '2', '3', '4', '5', '6', '7', '8', '9'], 1)) + ''.join(
        random.sample(num1, 4))
    qq_num = ''.join(random.sample(['1', '2', '3', '4', '5', '6', '7', '8', '9'], 1)) + ''.join(
        random.sample(num1, 8)) + '@qq.com'
    url = 'https://api.m.jd.com/client.action?appid=jd_shop_member&functionId=bindWithVender&body=%7B%22venderId%22%3A%22{4}%22%2C%22shopId%22%3A%22{7}%22%2C%22bindByVerifyCodeFlag%22%3A1%2C%22registerExtend%22%3A%7B%22v_sex%22%3A%22%E6%9C%AA%E7%9F%A5%22%2C%22v_name%22%3A%22{0}%22%2C%22v_birthday%22%3A%221990-03-18%22%2C%22v_email%22%3A%22{6}%22%7D%2C%22writeChildFlag%22%3A0%2C%22activityId%22%3A{5}%2C%22channel%22%3A{3}%7D&client=H5&clientVersion=9.2.0&uuid=&jsonp=jsonp_{1}_{2}'.format(
        v_name, timestamp, v_num1, channel, venderId, activityId, qq_num, shopId)
    try:
        async with httpx.AsyncClient(verify=False, headers=headers, timeout=30) as client:
            respon = await client.get(url=url)
        # respon = requests.get(url=url, verify=False, headers=headers, timeout=30)
        result = respon.text
        return result
    except Exception as e:
        try:
            print(e)
        finally:
            e = None
            del e


async def getResult(resulttxt, userName, user_num):
    r = re.compile('jsonp_.*?\\((.*?)\\)\\;', re.M | re.S | re.I)
    result = r.findall(resulttxt)
    for i in result:
        result_data = json.loads(i)
        busiCode = result_data['busiCode']
        if busiCode == '0':
            message = result_data['message']
            try:
                result = result_data['result']['giftInfo']['giftList']
                print(f"\t\t╰用户{user_num}【{userName}】:{message}")
                for i in result:
                    print('\t\t\t╰{0}:{1} '.format(i['prizeTypeName'], i['discount']))

            except:
                print(f"\t\t╰用户{user_num}【{userName}】:{message}")

            return busiCode
        print('\t\t╰用户{0}【{1}】:{2}'.format(user_num, userName, result_data['message']))
        return busiCode


async def exitCodeFun():
    try:
        exitCode = input('\n已结束..')
    except:
        pass


async def setHeaders(cookie, intype):
    if intype == 'mall':
        headers = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                   'Host': 'shop.m.jd.com',
                   'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.2 Safari/605.1.15',
                   'Accept-Language': 'zh-cn',
                   'Accept-Encoding': 'gzip, deflate, br',
                   'Connection': 'close'}
        return headers
    if intype == 'JDApp':
        headers = {'Cookie': cookie, 'Accept': '*/*',
                   'Connection': 'close',
                   'Referer': 'https://shopmember.m.jd.com/shopcard/?',
                   'Accept-Encoding': 'gzip, deflate, br',
                   'Host': 'api.m.jd.com',
                   'User-Agent': 'jdapp;iPhone;9.4.8;14.3;809409cbd5bb8a0fa8fff41378c1afe91b8075ad;network/wifi;ADID/201EDE7F-5111-49E8-9F0D-CCF9677CD6FE;supportApplePay/0;hasUPPay/0;hasOCPay/0;model/iPhone13,4;addressid/;supportBestPay/0;appBuild/167629;jdSupportDarkMode/0;Mozilla/5.0 (iPhone; CPU iPhone OS 14_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148;supportJDSHWK/1',
                   'Accept-Language': 'zh-cn'}
        return headers
    if intype == 'mh5':
        headers = {'Cookie': cookie, 'Accept': '*/*',
                   'Connection': 'close',
                   'Referer': 'https://shopmember.m.jd.com/shopcard/?',
                   'Accept-Encoding': 'gzip, deflate, br',
                   'Host': 'api.m.jd.com',
                   'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 14_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1',
                   'Accept-Language': 'zh-cn'}
        return headers


async def jd_main(activecode, Id):
    try:
        for ck in cks:
            ck, userName = await getUserInfo(ck, pinName='1')
            print(userName)
            headers_a = await setHeaders(ck, 'mh5')
            headers_b = await setHeaders(ck, 'mall')
            shopId = Id
            user_num = 1
            if activecode == 1:
                venderId = await getVenderId(Id, headers=headers_b)
            elif activecode == 2:
                venderId = Id
            else:
                print('id错误')
                break
            # print(shopId)
            # venderId =await getVenderId(shopId, headers=headers_b)
            activityId, getBean = await getShopOpenCardInfo(venderId, headers=headers_a, shopid=Id, userName=userName)
            # print(activityId, getBean)
            if activityId > 10:
                activityIdLabel = 1
                headers = await setHeaders(ck, 'JDApp')
                result = await bindWithVender(venderId, shopId, activityId, 208, headers)
                busiCode = await getResult(result, userName, user_num)
        print('-' * 50)
    except Exception as e:
        print(e)


#client = TelegramClient('test', api_id, api_hash, proxy=("socks5", '127.0.0.1', 7890))
client = TelegramClient('test', api_id, api_hash)
p1 = re.compile(r"[(](.*?)[)]", re.S)


async def guanzhu(url):
    for ck in cks:
        header = {
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.104 Safari/537.36",
            'Cookie': ck}
        async with httpx.AsyncClient(headers=header, verify=False, timeout=30) as client:
            r = await client.get(url=url)
        # r=requests.get(url=url,headers=header, verify=False)
        print(r.json()['result']['followDesc'])


async def get_id(url):
    # url='https://u.jd.com/qq3OS8s'
    global location1
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 14_5_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1 Mobile/15E148 Safari/604.1'
        }
        async with httpx.AsyncClient(headers=headers, verify=False, timeout=30) as client:
            pro_res = await client.get(url=url)
        # pro_res = requests.get(url, headers=headers, verify=False).text
        f = re.findall(r'(?<=hrl=\').+?(?=\';var)', pro_res.text)[0]
        # async with httpx.AsyncClient(headers=headers, verify=False, allow_redirects=False) as Client:
        # res=await Client.get(url=f)
        # location1=res.headers['location']
        location1 = requests.get(url=f, headers=headers, verify=False, allow_redirects=False).headers['location']

        # print(location1)
        Id = re.findall(r'(?<=Id=).+?(?=&)', location1)
        try:
            if 'shopId' in location1:
                print('shopId=' + Id[0])
                return (1, Id[0])
            elif 'venderId' in location1:
                print('verid=' + Id[0])
                return (2, Id[0])
            else:
                print('url err-getid')
                return (0, 0)
        except Exception as e:
            print(e)
    except Exception as e:
        print('网址错误！-getid')


# print(Id)
async def send_tg(chat_id, client, messages, m):
    destination_user_username = chat_id
    entity = await client.get_entity(destination_user_username)
    if m == 0:
        await client.send_message(entity=entity, message=messages)
    elif m == 1:
        await client.send_file(entity=entity, file=messages)
    else:
        print('发送错误')


async def optc(aus):
    try:
        url = 'https://api.jds.codes/jCommand'
        data = {"code": f"{aus}"}
        result = requests.post(url=url, json=data)
        if result.status_code == 200:
            jumpurl = result.json()['data']['jumpUrl']
            title = result.json()['data']['title']
            # url
            compile1 = re.compile('(?<=https:\/\/).+?(?=&)')
            url1 = re.findall(compile1, jumpurl)[0]
            # id
            compile2 = re.compile('(?<=activityId=).+?(?=&)')
            id1 = re.findall(compile2, jumpurl)[0]
            # url
            compile3 = re.compile('(?<=https:\/\/).+?(?=\/)')
            url2 = re.findall(compile3, jumpurl)[0]
            msg = f'原始url：{jumpurl}\n标题：{title}\n活动地址：{url1}\nid：{id1}\nurl：{url2}'
            print(msg)
            return msg
    except:
        return '我裂开了，看不懂你说的........'


# @client.on(events.NewMessage(incoming=True, chats=[-1001175133767]))
@client.on(events.NewMessage())
async def my_event_handler(event):
    print('1')
    sender = event.message.chat_id
    regex3 = re.compile(r"(集卡#.*)", re.M)
    open_url3 = re.findall(regex3, event.message.text)[0]
    if len(open_url3):
        mes = open_url3.split('#')
        if len(mes) == 3:
            msg = await optc(mes[-1])
            print(msg)
            await send_tg(sender, client, msg, 0)
        else:
            msg = '丢，别瞎搞'
            await send_tg(sender, client, msg, 0)
    '''
    try:
        regex1 = re.compile(r"(https://u.jd.com/.*)", re.M)
        open_url1 = re.findall(regex1, event.message.text)
        if len(open_url1):
            # if '入会' in event.raw_text:
            for j_url in open_url1:
                # print(j_url)
                # print(event.message.text)
                activecode, Id = await get_id(j_url)
                await jd_main(activecode, Id)
        # else:
        # print('等待关注程序开发！')
        regex2 = re.compile(r"(https://api.m.jd.com/.*)", re.M)
        open_url2 = re.findall(regex2, event.message.text)
        if len(open_url2):
            for j_url in open_url2:
                j_url = j_url.replace(')', '')
                # print(j_url)
                await guanzhu(j_url)
        regex3 = re.compile(r"(集卡#.*)", re.M)
        open_url3 = re.findall(regex3, event.message.text)[0]
        if len(open_url3):
            mes = open_url3.split('#')
            if len(mes) == 3:
                msg = await optc(mes[-1])
                print(msg)
                await send_tg(sender, client, msg, 0)
            else:
                msg = '丢，别瞎搞'
                await send_tg(sender, client, msg, 0)
    except Exception as e:
        print(e)
    '''

if __name__ == "__main__":
    with client:
        # client.loop.run_until_complete(main())
        client.loop.run_forever()
