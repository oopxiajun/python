'''
Created on 2019年11月19日

@author: Administrator
'''
list1 = [1,2,'str',{1,2,3}]
list2=["__",list1,0.1]

list3=list1+list2
print(list3)

list4=[1,2,3,4,5,6,7,8,9]
print(list4[1:6:1])             #从第二个到第七个（含第二个，不含第七个），步长为1
print(list4[1:6:2])             #从第二个到第七个（含第二个，不含第七个），步长为2
print(list4[1:6:3])             #从第二个到第七个（含第二个，不含第七个），步长为3


