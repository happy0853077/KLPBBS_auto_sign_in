# GitHub: https://github.com/xyz8848/KLPBBS_auto_sign_in

import http
import logging
import os
import smtplib
import sys
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from http import cookiejar

import requests
from bs4 import BeautifulSoup

username = os.environ.get("USERNAME")
password = os.environ.get("PASSWORD")

switch_user = int(os.environ.get("SWITCH_USER") or 0)
renewal_vip = int(os.environ.get("RENEWAL_VIP") or 0)
renewal_svip = int(os.environ.get("RENEWAL_SVIP") or 0)

debug = int(os.environ.get("DEBUG") or 0)

mail_enable = int(os.environ.get("MAIL_ENABLE") or 0)
mail_host = os.environ.get("MAIL_HOST")
mail_port = int(os.environ.get("MAIL_PORT") or 0)
mail_username = os.environ.get("MAIL_USERNAME")
mail_password = os.environ.get("MAIL_PASSWORD")
mail_to = os.environ.get("MAIL_TO") or []

serverchan_enable = int(os.environ.get("SERVERCHAN_ENABLE") or 0)
serverchan_key = os.environ.get("SERVERCHAN_KEY")

# 设置日志级别和格式
if debug == 1:
    logging.basicConfig(level=logging.DEBUG, format='[%(levelname)s] [%(asctime)s] %(message)s')
    logging.info("Debug mode enabled.")
else:
    logging.basicConfig(level=logging.INFO, format='[%(levelname)s] [%(asctime)s] %(message)s')
    logging.info("Debug mode disabled.")

userAgent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36 Edg/116.0.1938.81'

header = {
    "origin": "https://klpbbs.com",
    "Referer": "https://klpbbs.com/",
    'User-Agent': userAgent,
}

session = requests.session()
session.cookies = http.cookiejar.LWPCookieJar()


def login(username, password):
    post_url = "https://klpbbs.com/member.php?mod=logging&action=login&loginsubmit=yes"
    post_data = {
        "username": username,
        "password": password,
    }

    response_res = session.post(post_url, data=post_data, headers=header)
    logging.debug(f"statusCode = {response_res.status_code}")
    logging.debug(f"https://klpbbs.com/member.php?mod=logging&action=login&loginsubmit=yes = {response_res.text}")

    header["Cookie"] = "; ".join([f"{cookie.name}={cookie.value}" for cookie in session.cookies])
    # logging.debug(f'Header: {header}')

    # soup = BeautifulSoup(response_res.text, 'html.parser')
    # a_tag = soup.find('a', href_='https://klpbbs.com/')
    # if a_tag is not None:
    #     logging.info('登录成功')
    # else:
    #     logging.info('登陆失败')
    #     exit(1)


def get_url():
    html_source = session.get('https://klpbbs.com/')
    logging.debug(html_source.text)
    soup = BeautifulSoup(html_source.text, 'html.parser')
    a_tag = soup.find('a', class_='midaben_signpanel JD_sign')
    if a_tag is not None:
        href_value = a_tag['href']
        sign_in_url = 'https://klpbbs.com/' + href_value

        logging.debug(f'签到链接：{sign_in_url}')

        if sign_in_url == 'https://klpbbs.com/member.php?mod=logging&action=login':
            logging.info('签到链接异常（原因：登陆失败）')
            exit(1)

        logging.info('已成功获取签到链接')

        return sign_in_url
    else:
        is_sign_in()
        return None


def sign_in(sign_in_url):
    session.get(sign_in_url, headers=header)


def is_sign_in():
    html_source = session.get('https://klpbbs.com/')
    logging.debug(f'https://klpbbs.com/ = {html_source.text}')
    soup = BeautifulSoup(html_source.text, 'html.parser')
    a_tag = soup.find('a', class_='midaben_signpanel JD_sign visted')
    if a_tag is not None:
        href_value = a_tag['href']
        if href_value == 'k_misign-sign.html':
            logging.info('已成功签到')
            notice('苦力怕论坛自动签到：已成功签到！')
            exit(0)
        else:  # 异常处理
            # 用户组到期处理
            div_tag = soup.find('div', class_='notice')
            if div_tag == '您当前的用户组已经到期，请选择继续续费还是要切换到其他用户组':
                if switch_user == 1:
                    session.get(
                        'https://klpbbs.com/home.php?mod=spacecp&ac=usergroup&do=switch&groupid=10&handlekey=switchgrouphk',
                        headers=header)
                    logging.info('已切换回普通用户组')
                    notice('苦力怕论坛自动签到：已切换回普通用户组')
                elif renewal_vip == 1:
                    session.get(
                        'https://klpbbs.com/home.php?mod=spacecp&ac=usergroup&do=buy&groupid=21&inajax=1',
                        headers=header)
                    logging.info('已续费VIP')
                    notice('苦力怕论坛自动签到：已续费VIP')
                    os.execl(sys.executable, sys.executable, *sys.argv)
                elif renewal_svip == 1:
                    session.get(
                        'https://klpbbs.com/home.php?mod=spacecp&ac=usergroup&do=buy&groupid=22&inajax=1',
                        headers=header)
                    logging.info('已续费SVIP')
                    notice('苦力怕论坛自动签到：已续费SVIP')
                    os.execl(sys.executable, sys.executable, *sys.argv)
                else:
                    logging.info(f'签到失败（原因：当前用户组已到期）')
                    notice('苦力怕论坛自动签到：签到失败（原因：当前用户组已到期）')
                    exit(1)

            logging.info('签到失败')
            notice('苦力怕论坛自动签到：签到失败')
            exit(1)
    else:
        logging.info('签到失败')
        notice('苦力怕论坛自动签到：签到失败')
        exit(1)


def notice(msg):
    if mail_enable == 1:
        email_notice(msg)
    if serverchan_enable == 1:
        serverchan_notice(msg)


def email_notice(msg):
    message = MIMEMultipart()
    message['From'] = mail_username
    message['To'] = mail_to
    message['Subject'] = msg
    body = f"{msg}<br><br>Powered by <a href='https://github.com/xyz8848/KLPBBS_auto_sign_in'>https://github.com/xyz8848/KLPBBS_auto_sign_in</a>"
    message.attach(MIMEText(body, "html"))

    try:
        server = smtplib.SMTP(mail_host, mail_port)
        server.starttls()
        server.login(mail_username, mail_password)
        server.send_message(message)
        logging.info('邮件发送成功')
    except smtplib.SMTPException as error:
        logging.info('邮件发送失败')
        logging.error(error)


def serverchan_notice(msg):
    url = f"https://sctapi.ftqq.com/{serverchan_key}.send"
    data = {
        "title": "苦力怕论坛自动签到",
        "desp": msg
    }
    try:
        response = requests.post(url, data=data)
        logging.debug(response.text)
        logging.info('Server酱消息发送成功')
    except requests.RequestException as error:
        logging.info('Server酱消息发送失败')
        logging.error(error)


if __name__ == '__main__':
    logging.debug(f'UserAgent: {userAgent}')

    login(username, password)

    url = get_url()

    sign_in(url)

    is_sign_in()
