# [KLPBBS_auto_sign_in](https://github.com/xyz8848/KLPBBS_auto_sign_in)
基于 GitHub Action 的苦力怕论坛自动签到脚本  
[![GitHub Stars](https://img.shields.io/github/stars/xyz8848/KLPBBS_auto_sign_in)](https://github.com/xyz8848/KLPBBS_auto_sign_in/stargazers)
[![GitHub Forks](https://img.shields.io/github/forks/xyz8848/KLPBBS_auto_sign_in)](https://github.com/xyz8848/KLPBBS_auto_sign_in/network/members)

## 如何使用

1. [Fork](https://github.com/xyz8848/KLPBBS_auto_sign_in/fork) 这个仓库
2. 打开 Actions secrets and variables  
![](https://cdn.xyz8848.com/img/github/KLPBBS_auto_sign_in/1.png)
3. 添加以下 secret：`USERNAME`，`PASSWORD`（[点击查看更多内容](https://github.com/xyz8848/KLPBBS_auto_sign_in/blob/main/docs/secrets.md)）

## 更多功能
### 自定义签到时间
（默认每天 00:01 签到）
1. 到 [`.github/workflows/sign_in.yml`](.github/workflows/sign_in.yml) 中修改签到时间

### 签到后邮件提示
1. 打开 Actions secrets and variables
2. 添加以下 secret：`MAIL_ENABLE`，`MAIL_HOST`，`MAIL_PORT`，`MAIL_USERNAME`，`MAIL_PASSWORD`，`MAIL_TO`（[点击查看更多内容](https://github.com/xyz8848/KLPBBS_auto_sign_in/blob/main/docs/secrets.md)）

### 签到后企业微信提示
_施工中_
