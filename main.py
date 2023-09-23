# GitHub: https://github.com/xyz8848/KLPBBS_auto_sign_in

import http
import logging
import os
from http import cookiejar

import requests
from bs4 import BeautifulSoup

username = os.environ["USERNAME"]

password = os.environ["PASSWORD"]

debug = os.environ["DEBUG"]

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

    # TODO 判断是否登录成功


def get_html():
    html_source = session.get('https://klpbbs.com/')
    logging.debug(html_source.text)
    return html_source


def get_url(html_source):
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
        is_sign_in(html_source)
        return None


def sign_in(sign_in_url):
    session.get(sign_in_url, headers=header)


def is_sign_in(html_source):
    soup = BeautifulSoup(html_source.text, 'html.parser')
    a_tag = soup.find('a', class_='midaben_signpanel JD_sign visted')
    if a_tag is not None:
        href_value = a_tag['href']
        if href_value == 'k_misign-sign.html':
            logging.info('已成功签到')
            exit(0)
        else:
            logging.info('签到失败')
    else:
        logging.info('签到失败')


# TODO
def email_notice():
    ...


if __name__ == '__main__':
    logging.debug(f'UserAgent: {userAgent}')

    login(username, password)

    html = get_html()

    url = get_url(html)

    sign_in(url)

    is_sign_in(html)
