import requests

# 会话
session = requests.session()#新建一个session对象
# 我们的登录信息
data = {
    "loginName": "188888881",#帐号
    "password": "123456"#密码
}
# 1. 登录
url = "https://passport.17k.com/ck/user/login"#登录接口rul
session.post(url, data=data)#模拟登陆
# print(session.text)
print(session.cookies)  # 查看cookie

# 2. 拿书架上的数据
# 刚才的那个session中是有cookie的
resp = session.get('https://user.17k.com/ck/author/shelf?page=1&appKey=2406394919')

print(resp.json())
