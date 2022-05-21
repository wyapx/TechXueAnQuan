# TechXueAnQuan
### 使用高科技帮你解决安全教育平台 ：）

### 目前支持：
 - [x] 多账户支持
 - [x] 账号密码登录
 - [x] 自动观看视频
 - [ ] 自动完成选择题
 - [ ] 在GitHub CI中运行

### 食用方法
#### 0.准备环境

 - Python3.6以上
 - 一个会用`cmd`/`bash`的正常人

#### 1.创建配置文件

创建一个config.json，按以下格式写入你的账号密码
```json
[
  ["Username1", "Password1"],
  ["Username2", "Password2"]
]
```

注：账号中有大量个人信息，请妥善保管

#### 2.开始运行

```shell
python3 main.py /path/to/config.json
# or
py main.py /path/to/config.json
```

### 写在最后

如果你觉得这个软件对你的学习有帮助的话  
请点一下右上角的Star ~~(star不要钱)~~  
