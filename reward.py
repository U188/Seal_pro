import requests, re, json, os,datetime
def nowtime():
	h=datetime.datetime.now().strftime('%H')
	if int(h)<15:
		return 20
	else:
		return 500
def joy():
    JD_JOY_REWARD_NAME = str(nowtime())
    if JD_JOY_REWARD_NAME:
        msg = f"宠旺旺兑换数量：{JD_JOY_REWARD_NAME}\n"
        with open(f"{env}/config/config.sh", 'r', encoding='utf-8') as f1:
            configs = f1.read()
        if "export JD_JOY_REWARD_NAME=" in configs:
            if 'JD_JOY_REWARD_NAME="{JD_JOY_REWARD_NAME}"' in configs:
                msg += "宠旺旺兑换数量相同，取消替换"
                return msg
            configs = re.sub(f'JD_JOY_REWARD_NAME=(\"|\').*(\"|\')', f'JD_JOY_REWARD_NAME="{JD_JOY_REWARD_NAME}"', configs)
            if JD_JOY_REWARD_NAME in configs:
                msg += "替换宠旺旺兑换数量成功"
            else:
                msg += "替换宠旺旺兑换数量失败，请手动替换"
        else:
            msg += "程序没有找到设置宠旺旺兑换的变量值，将自动添加进配置"
            export =  f"export JD_JOY_REWARD_NAME={JD_JOY_REWARD_NAME} # 宠旺旺兑换数量\n"
            if 'jd' in env:
                with open(f"{env}/config/config.sh", 'r', encoding='utf-8') as f3:
                    configs = f3.readlines()
                for config in configs:
                    if config.find("第五区域") != -1 and config.find("↓") != -1:
                        end_line = configs.index(config)
                        break
                configs.insert(end_line + 4, export)
                configs = ''.join(configs)
            elif 'ql' in env:
                configs += export
        with open(f"{env}/config/config.sh", 'w', encoding='utf-8') as f2:
            f2.write(configs)
        return msg
    else:
        msg = "无法从页面读取宠旺旺兑换数量，无法完成替换"
        return msg


def findCrontab():
    crontab_list = f'{env}/config/crontab.list'
    with open(crontab_list, 'r', encoding='utf-8') as f1:
        crontabs = f1.readlines()
    for crontab in crontabs:
        if crontab.find("jd_dreamFactory") != -1:
            cron = ' '.join(crontab.split(" ")[:5])
            return cron
    return False


def checkCrontab():
    storage = '/' + path_list[-2]
    file = '/' + path_list[-1]
    crontab_list = f'{env}/config/crontab.list'
    key = '# 获取宠旺旺兑换数量（请勿删除此行）\n'
    new = f'{cron} python /jd{storage}{file} >> /jd/log{file.split(".")[0]}.log 2>&1\n'
    with open(crontab_list, 'r', encoding='utf-8') as f1:
        crontab = f1.readlines()
    if crontab[-1] == '\n':
        del (crontab[-1])
    if key in crontab:
        m = crontab.index(key) + 1
        if crontab[m] != new:
            crontab[m] = new
            with open(crontab_list, 'w', encoding='utf-8') as f2:
                print(''.join(crontab), file=f2)
        else:
            return
    else:
        crontab.append(f'\n{key}{new}')
        with open(crontab_list, 'w', encoding='utf-8') as f2:
            print(''.join(crontab), file=f2)


def tgNofity(user_id, bot_token, text):
    TG_API_HOST = 'api.telegram.org'
    url = f'https://{TG_API_HOST}/bot{bot_token}/sendMessage'
    body = {
        "chat_id": user_id,
        "text": text,
        "disable_web_page_preview": True
    }
    headers = {
        "ontent-Type": "application/x-www-form-urlencoded"
    }
    try:
        r = requests.post(url, data=body, headers=headers)
        if r.ok:
            print("Telegram发送通知消息成功🎉。\n")
        elif r.status_code == '400':
            print("请主动给bot发送一条消息并检查接收用户ID是否正确。\n")
        elif r.status_code == '401':
            print("Telegram bot token 填写错误。\n")
    except Exception as error:
        print(f"telegram发送通知消息失败！！\n{error}")


# 开始执行主程序
if __name__ == '__main__':
    path_list = os.path.realpath(__file__).split('/')[1:]
    env = '/' + '/'.join(path_list[:-2])
    if os.path.isfile('/ql/config/cookie.sh') or os.path.isfile(f'{env}/config/cookie.sh'):  # 青龙
        isv4 = False
        if not os.path.isfile(f'{env}/config/cookie.sh'):  # 青龙容器内
            env = '/ql'
    else:  # v4-bot
        isv4 = True
        if not os.path.isfile(f'{env}/config/config.sh'):  # v4-bot 容器内
            env = '/jd'
    cron = '此处填写' # 此处 V4 用户需要自行设置 cron 表达式，否则程序自动设置为 jd_dreamFactory.js 的运行时间
    if 'jd' in env:
        if len(cron) < 9:
            cron = findCrontab()
        if not cron:
            cron = "0 0,7,20 * * *"
        checkCrontab()
    msg = joy()
    print(msg)
    try:
        bot = f'{env}/config/bot.json'
        with open(bot, 'r', encoding='utf-8') as botSet:
            bot = json.load(botSet)
        tgNofity(bot['user_id'], bot['bot_token'], msg)
    except:
        None