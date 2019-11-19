'''
Created on 2019年11月19日

@author: Administrator
''' 
num=1.1
print(isinstance(num, int))         #False
print(isinstance(num, float))       #True
print(isinstance(num, bool))        #False
print(isinstance(num, complex))     #False
num=2
print(isinstance(num, int))         #True

a=1
b=2.2
d=2
c=a+b
print (c)

c=a/d       #结果是小数
print (c)

c=a//d      #结果是求商（类似于c#的）
print (c)

c=a%d       #结果是求余数（求模）
print (c)

print(3 * 7)
print(2 ** 3)
print(2 ** 5)
"""
isinstance 和 type 的区别在于：
    type()不会认为子类是一种父类类型。
    isinstance()会认为子类是一种父类类型。
"""