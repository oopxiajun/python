# pip install requests

import requests    
import re
import json


base_url = 'https://www.eagle-sight.com/NewEnergy/'
headers ={}# {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
requests.packages.urllib3.disable_warnings()
response = requests.get(base_url, headers=headers,verify=False)
#在输出结果前先设置内容编码
response.encoding = "utf-8"
data = response.text
print(data)
# pattern = re.compile('<h2><a target="_blank" href="(.*?)">(.*?)</a></h2>', re.S)
# pattern_list = pattern.findall(data)  # -->list

# # json [{[]}]{}
# # 构建json数据格式
# data_list = []

# for i in pattern_list:
#     data_dict = {}
#     data_dict['title'] = i[1]
#     data_dict['href'] = i[0]
#     print(data_dict)
#     data_list.append(data_dict)
# print (data_list)