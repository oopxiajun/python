'''
Created on 2019年11月19日

@author: Administrator
'''
a, b, c, d = 20, 5.5, True, 4+3j
print(a,b,c,d)
print(type(a), type(b), type(c), type(d))
"""
20 5.5 True (4+3j)
<class 'int'> <class 'float'> <class 'bool'> <class 'complex'>
"""

compare = isinstance(a, int)
print(compare)

compare = isinstance(a, float)
print(compare)