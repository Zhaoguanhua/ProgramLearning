#!usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Author  : zhaoguanhua
@Email   : zhaogh@hdsxtech.com
@Time    : 2020/1/16 17:36
@File    : generater_test.py
@Software: PyCharm
"""

"""
迭代器、生成器测试
"""
import sys

#***************************************************************
#迭代器
"""
迭代取值，内置__iter__和__next__方法
可以用next()方法访问，也可以用for循环访问
"""
class Fib:
    def __init__(self, n):
        self.prev = 0
        self.cur = 1
        self.n = n

    def __iter__(self):
        return self

    def __next__(self):
        if self.n > 0:
            value = self.cur
            self.cur = self.cur + self.prev
            self.prev = value
            self.n -= 1
            return value
        else:
            raise StopIteration()

f = Fib(10)
print([i for i in f])

#***************************************************************
#生成器
"""
生成器是一种简单的迭代器，使用yeild关键字
yeild和return都可以返回值，但是return只能返回一次，yeild能返回多次
可以用next()方法访问，也可以用for循环访问
"""
def fib(n):
    prev, curr = 0, 1
    while n > 0:
        n -= 1
        yield curr
        prev, curr = curr, curr + prev

a=fib(10)

res1 = next(a)
print(res1)
res2 = next(a)
print(res2)
res3 = next(a)
print(res3)
res4 = next(a)
print(res4)

#***************************************************************
#生成器表达式
g=(i**2 for i in range(1,6) if i >3)
print(g)
print(next(g))
print(next(g))

#***************************************************************
#列表生成式
l=[i**2 for i in range(1,6) if i >3]
print(l)



