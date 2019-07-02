#!/usr/bin/env python3
# -*- coding:utf-8 -*-


import requests
import smtplib
from email.mime.text import MIMEText
from apscheduler.schedulers.blocking import BlockingScheduler

mail_host = "smtp.163.com"  # SMTP服务器
mail_user = "your Email"  # 用户名
mail_pass = "password"  # 密码
receivers = ['306931275@qq.com']  # 接收邮件，可设置为你的QQ邮箱或者其他邮箱
title = 'Python SMTP Mail Test'  # 邮件主题
content = '网站崩溃了'
url1 = "http://192.168.2.39/"
url2 = "http://www.jisu.edu.cn/"


def send_email(abc, from_email, password, to_email, etitle, econtent):
    mail_host = abc  # SMTP服务器
    mail_user = from_email  # 用户名
    mail_pass = password  # 密码
    sender = from_email  # 发件人邮箱(最好写全, 不然会失败)
    receivers = to_email  # 接收邮件，可设置为你的QQ邮箱或者其他邮箱
    content = econtent
    title = etitle  # 邮件主题

    message = MIMEText(content, 'plain', 'utf-8')  # 内容, 格式, 编码
    message['From'] = "{}".format(sender)
    message['To'] = ",".join(receivers)
    message['Subject'] = title

    try:
        smtpObj = smtplib.SMTP_SSL(mail_host, 465)  # 启用SSL发信, 端口一般是465
        smtpObj.login(mail_user, mail_pass)  # 登录验证
        smtpObj.sendmail(sender, receivers, message.as_string())  # 发送
        print("mail has been send successfully.")
    except smtplib.SMTPException as e:
        print(e)


def request_access(u):
    try:
        r = requests.get(u, timeout=5)
        code = r.status_code
        if code == 200:
            print(str(u) + "网站访问正常")
        else:
            print(str(u) + "不能访问！")

            send_email(mail_host, mail_user, mail_pass, receivers, title, content)
    # except(ConnectionRefusedError, AttributeError):
    except requests.exceptions.Timeout:
        send_email(mail_host, mail_user, mail_pass, receivers, title, content)
        print(str(u) + "网络异常")


def request_url1():
    global url1
    request_access(url1)


def request_url2():
    global url2
    request_access(url2)


sched = BlockingScheduler()
sched.add_job(request_url1, 'interval', seconds=3)
sched.add_job(request_url2, 'interval', seconds=3)

try:
    sched.start()
except(KeyboardInterrupt, SystemExit, SystemError):
    pass
