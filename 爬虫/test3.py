import lxml
import requests
from bs4 import BeautifulSoup

html =  """
<html><head><title>The Dormouse's story</title></head>
<body>
<p class="title"><b>The Dormouse's story</b></p>
<p class="story">Once upon a time there were three little sisters; and their names were
<a href="http://example.com/elsie" class="sister" id="link1"><!--Elsie--></a>,
<a href="http://example.com/lacie" class="sister" id="link2">Lacie</a> and
<a href="http://example.com/tillie" class="sister" id="link3">Tillie</a>;
and they lived at the bottom of a well.</p>
<p class="story">...</p>
"""
base_url = 'https://www.eagle-sight.com/NewEnergy/'
headers ={}# {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
requests.packages.urllib3.disable_warnings()
response = requests.get(base_url, headers=headers,verify=False)
#在输出结果前先设置内容编码
response.encoding = "utf-8"
html = response.text
#1、BeautifulSoup对象
soup = BeautifulSoup(html,'lxml')
print(type(soup))

#2、Tag对象
print(soup.head)
print(soup.head.name)
print(soup.head.attrs)
print(type(soup.head),'\n')

#3、Navigable String对象
print(soup.title.string)
print(type(soup.title.string),'\n')


print(soup.body)
print(soup.body.name)
print(soup.body.string)
print(soup.body.prettify())

# #4、Comment对象
# print(soup.a.string,'\n')
# print(type(soup.a.string))

#5、结构化输出soup对象
print(soup.prettify())