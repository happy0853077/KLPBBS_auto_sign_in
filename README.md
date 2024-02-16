# [KLPBBS_auto_sign_in](https://github.com/xyz8848/KLPBBS_auto_sign_in)
基于 GitHub Action 的苦力怕论坛自动签到脚本  
[![GitHub Stars](https://img.shields.io/github/stars/xyz8848/KLPBBS_auto_sign_in)](https://github.com/xyz8848/KLPBBS_auto_sign_in/stargazers)
[![GitHub Forks](https://img.shields.io/github/forks/xyz8848/KLPBBS_auto_sign_in)](https://github.com/xyz8848/KLPBBS_auto_sign_in/network/members)

## 如何使用

1. [Fork](https://github.com/xyz8848/KLPBBS_auto_sign_in/fork) 这个仓库
2. 授予工作流读取和写入权限（用于工作流保活，如果仓库中在过去 60 天内没有提交，GitHub 将暂停 GitHub 工作流的计划触发器。除非进行新的提交，否则基于 cron 的触发器不会运行。）
![step2.webp](img/step2.webp)
3. 打开 Actions secrets and variables  
![step3.webp](img/step3.webp)
4. 添加以下 secret：`USERNAME`，`PASSWORD`（[点击查看更多内容](https://github.com/xyz8848/KLPBBS_auto_sign_in/blob/main/docs/secrets.md)）

## 更多功能
### 自定义签到时间
（默认每天 00:01 签到）
1. 到 [`.github/workflows/sign_in.yml`](.github/workflows/sign_in.yml) 中修改签到时间

### 签到后邮件提示
1. 打开 Actions secrets and variables
2. 添加以下 secret：`MAIL_ENABLE`，`MAIL_HOST`，`MAIL_PORT`，`MAIL_USERNAME`，`MAIL_PASSWORD`，`MAIL_TO`（[点击查看更多内容](https://github.com/xyz8848/KLPBBS_auto_sign_in/blob/main/docs/secrets.md)）

### 签到后企业微信提示
_施工中_

### 签到后Server酱提示
1. 打开 Actions secrets and variables
2. 添加以下 secret：`SERVERCHAN_ENABLE`，`SERVERCHAN_KEY`（[点击查看更多内容](https://github.com/xyz8848/KLPBBS_auto_sign_in/blob/main/docs/secrets.md)）
