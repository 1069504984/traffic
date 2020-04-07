# -*- coding: utf-8 -*-
# @Time    : 2019/12/9 19:54
# @Author  : Fighter
from ddt import ddt,data
import re
p=r'[1-9]{1,3}(\.[0-9]{1,3}){3}'
T="127.0.0.1 172.0.0.10"
M=re.findall(p,T)
print(M)

p1=r'([1-9]{1,3}(\.[0-9]{1,3}){3})'
print(re.findall(p1,T))