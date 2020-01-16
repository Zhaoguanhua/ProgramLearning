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

#迭代器
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

#生成器
def fib(n):
    prev, curr = 0, 1
    while n > 0:
        n -= 1
        yield curr
        prev, curr = curr, curr + prev

print([i for i in fib(10)])