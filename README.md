# [KLPBBS_auto_sign_in](https://github.com/xyz8848/KLPBBS_auto_sign_in)
基于 GitHub Action 的苦力怕论坛自动签到脚本

## 如何使用

1. [Fork](https://github.com/xyz8848/KLPBBS_auto_sign_in/fork) 这个仓库
2. 打开 Actions secrets and variables  
![](https://cdn.xyz8848.com/img/github/KLPBBS_auto_sign_in/1.png)
3. 添加以下 secret：`USERNAME`，`PASSWORD`，`DEBUG` （[点击查看更多内容](https://github.com/xyz8848/KLPBBS_auto_sign_in/blob/main/docs/secrets.md)）
4. 到 [`.github/workflows/sign_in.yml`](.github/workflows/sign_in.yml) 中修改签到时间（默认每天 08:01 签到）

## TODO
- [ ] 判断是否签到成功
- [ ] 邮箱返回签到结果