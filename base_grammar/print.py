'''
Created on 2019年11月19日

@author: Administrator
'''
print()                 #空行
print ("Hello, Python!")

my_str="Hello Python，I am oopxiajun！"

print(my_str)           #输出所有内容
print(my_str[0])        #输出第一个字符
print(my_str[1:2])      #输出第二个到第三个字符串（包好第二个 ，不含第三个）
print(my_str[5:])       #输出第6个字符以后的所有字符（包含第六个）
print(my_str[:-4])      #输出第一个到倒数第四个字符之间的所有字符（包含第一个 ，不含 倒数第四个）

print(my_str * 5)       #五次输出字符串

print(my_str +"这是拼接上的内容！")  #输出是拼接

print('hello\noopxiajun!!!!')  # 使用反斜杠(\)+n转义特殊字符(换行)

print(r"hello\noopxiajun!!!!")  # 使用反斜杠(\)+n转义特殊字符(换行)


# 不换行输出
print( "大爷，",end="")
print( "来玩玩呗！！！！", "")