'''
Created on 2019年11月19日

@author: Administrator
'''
"""
在 python 用 import 或者 from...import 来导入相应的模块。(类似于C#的using，java中的import)

将整个模块(somemodule)导入，格式为： import somemodule(类似于C#的using somemodule，java中的import somemodule)

从某个模块中导入某个函数,格式为： from somemodule import somefunction

从某个模块中导入多个函数,格式为： from somemodule import firstfunc, secondfunc, thirdfunc

将某个模块中的全部函数导入，格式为： from somemodule import *

"""

import sys
from sys import argv,path  #  导入特定的成员（可在顶部导入，也可在使用的时候导入）

for item in sys.argv:
    print(item) #当前文件信息
    

from sys import argv,path  #  导入特定的成员
print('================python from import===================================')
print('path:',path) # 因为已经导入path成员，所以此处引用时不需要加sys.path