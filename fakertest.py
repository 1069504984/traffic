# -*- coding: utf-8 -*-
# @Time    : 2019/12/2 11:37
# @Author  : Fighter
from faker import Faker

test = Faker(locale='zh-cn')
l = []
for i in range(100):
    name = test.name()
    l.append(name)
print(l)
print(len(l))
print(test.name())
