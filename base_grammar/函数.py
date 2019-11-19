'''
Created on 2019年11月19日

@author: Administrator
函数是组织好的，可重复使用的，用来实现单一，或相关联功能的代码段。
'''


def sayHello(name):
    print("Hello " + name)

    
# 计算面积函数
def area(width, height):
    return width * height


sayHello("oopxiajun")
sayHello(name="夏军")
w = 1.2
h = 2.1
print("面积：", area(w, h))


# 传不可变对象实例
def ChangeInt(a1):
    a1 = 10
    return


# 可写函数说明
def changeme(mylist):
   "修改传入的列表"
   mylist.append([1, 2, 3, 4])
   print ("函数内取值: ", mylist)
   return


b = 2
ChangeInt(b)
print(b)

# 调用changeme函数
mylist = [10, 20, 30]
changeme(mylist)
print ("函数外取值: ", mylist)


# 可写函数说明
def printinfo(*vartuple):
   "打印任何传入的参数"
   print ("输出: ") 
   print (vartuple)

   
printinfo()
printinfo(1)
printinfo(1, 2)
printinfo([1, 2, 3])
printinfo({1, 2, 3})

#加了两个星号 ** 的参数会以字典的形式导入。
#可写函数说明
def printinfo_1(**vardict ):
   "打印任何传入的参数"
   print ("输出: ") 
   print (vardict)
   

#printinfo_1()
#printinfo_1(1)
#printinfo_1(1, 2)
#printinfo_1([1, 2, 3])
#printinfo_1({1, 2, 3})
printinfo_1(a=1, b=2)

#匿名函数
sum = lambda arg1, arg2: arg1 + arg2
print ("相加后的值为 : ", sum( 10, 20 ))
