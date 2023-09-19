#!/usr/bin/python
# -*- coding: UTF-8 -*-

class  A:
    def methodA(self):
        print('我是基类A')

class  B:
    def methodB(self):
        print('我是基类B')

class C(A,B):
    def methodC(self):
        print('我是子类C')

c= C()
c.methodA()
c.methodB()
c.methodC()

