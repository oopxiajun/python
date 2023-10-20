import requests
url = 'https://admin.yueyuechuxing.cn/oss?bucket=yycx-assets&name=license/1001/20230916/68/1694867266553_temp.jpg'
res = requests.get(url)

with open('pythonimage.png', 'wb') as f:
    f.write(res.content)