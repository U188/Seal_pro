import os,smtplib,datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header
from email.utils import formataddr

POST_EMAIL=''
GET_EMAIL=''
PASSWORD=''
if POST_EMAIL in os.environ and os.environ["POST_EMAIL"] and GET_EMAIL in os.environ and os.environ['GET_EMAIL'] and PASSWORD in os.environ and os.environ['PASSWORD']:
    POST_EMAIL = os.environ["POST_EMAIL"]
    GET_EMAIL = os.environ['GET_EMAIL']
    PASSWORD = os.environ['PASSWORD']
    print('邮件推送打开！')

def send_email():
    POST_EMAIL = os.environ["POST_EMAIL"]
    GET_EMAIL = os.environ['GET_EMAIL']
    PASSWORD = os.environ['PASSWORD']
    mail_host = "smtp.qq.com"  # 设置服务器
    mail_user = POST_EMAIL  # 用户名
    mail_pass = PASSWORD  # 口令
    sender = POST_EMAIL  # 发送者的邮箱
    receivers = GET_EMAIL  # 接收邮件，其他人的邮箱
    # 创建一个带附件的实例
    message = MIMEMultipart()
    message["From"] = formataddr(["smtp", sender])  # 发送人
    message["To"] = formataddr(["", receivers[0]])  # 接收人
    subject = '邮件'
    message['Subject'] = Header(subject, 'utf-8')  # 邮件主题
    # 邮件正文内容
    message.attach(MIMEText('seal最新--'+str(datetime.date.today(), 'plain', 'utf-8'))
    # 构造附件1，传送当前目录下的 test.txt 文件
    att1 = MIMEText(open(str(datetime.date.today())+'.txt', 'rb').read(), 'base64', 'utf-8')
    att1["Content-Type"] = 'application/octet-stream'
    # 这里的filename可以任意写，写什么名字，邮件中显示什么名字
    att1["Content-Disposition"] = 'attachment; filename="Seal.txt"'
    message.attach(att1)
    try:
        smtpObj = smtplib.SMTP_SSL(host=mail_host)
        smtpObj.connect(mail_host, 465)
        smtpObj.login(mail_user, mail_pass)
        smtpObj.sendmail(sender, receivers, message.as_string())
        smtpObj.quit()
    except smtplib.SMTPException:
        print("发送失败！")
