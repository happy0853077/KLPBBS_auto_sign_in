# GitHub: https://github.com/xyz8848/KLPBBS_auto_sign_in

import http
import logging
import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from http import cookiejar

import requests
from bs4 import BeautifulSoup

username = os.environ.get("USERNAME")
password = os.environ.get("PASSWORD")

debug = int(os.environ.get("DEBUG") or 0)

mail_enable = int(os.environ.get("MAIL_ENABLE") or 0)
mail_host = os.environ.get("MAIL_HOST")
mail_port = int(os.environ.get("MAIL_PORT") or 0)
mail_username = os.environ.get("MAIL_USERNAME")
mail_password = os.environ.get("MAIL_PASSWORD")
mail_to = os.environ.get("MAIL_TO") or []

# 设置日志级别和格式
if debug == 1:
    logging.basicConfig(level=logging.DEBUG, format='[%(levelname)s] [%(asctime)s] %(message)s')
else:
    logging.basicConfig(level=logging.INFO, format='[%(levelname)s] [%(asctime)s] %(message)s')

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
    logging.debug(f"text = {response_res.text}")

    header["Cookie"] = "; ".join([f"{cookie.name}={cookie.value}" for cookie in session.cookies])
    # logging.debug(f'Header: {header}')

    soup = BeautifulSoup(response_res.text, 'html.parser')
    a_tag = soup.find('a', href_='https://klpbbs.com/')
    if a_tag is not None:
        logging.info('登录成功')
    else:
        logging.info('登陆失败')
        exit(101)


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
            logging.info('签到链接异常')
            exit(100)

        logging.info('已成功获取签到链接')

        return sign_in_url
    else:
        is_sign_in()
        return None


def sign_in(sign_in_url):
    session.get(sign_in_url, headers=header)


def is_sign_in():
    html_source = session.get('https://klpbbs.com/')
    logging.debug(html_source.text)
    soup = BeautifulSoup(html_source.text, 'html.parser')
    a_tag = soup.find('a', class_='midaben_signpanel JD_sign visted')
    if a_tag is not None:
        href_value = a_tag['href']
        if href_value == 'k_misign-sign.html':
            logging.info('已成功签到')
            email_notice('苦力怕论坛自动签到：已成功签到！')
        else:
            logging.info('签到失败')
            email_notice('苦力怕论坛自动签到：签到失败')
    else:
        logging.info('签到失败')
        email_notice('苦力怕论坛自动签到：签到失败')


def email_notice(msg):
    if mail_enable == 0:
        return None
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


if __name__ == '__main__':
    logging.debug(f'UserAgent: {userAgent}')

    login(username, password)

    url = get_url()

    sign_in(url)

    is_sign_in()
