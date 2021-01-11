# -*- coding: utf-8 -*-
# @Time    : 2019/12/10 16:16
# @Author  : Fighter
import random

import requests
import os
import json




cookies = {
    'com.wibu.cm.webadmin.lang': 'zh-CN',
}


headers = {
    'Connection': 'keep-alive',
    'Accept': 'application/json, text/plain, */*',
    'Origin': 'http://172.16.1.147:8000',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36',
    'token': '1dd3b1347a8c4a0cae5eb902ddf82826',
    'Content-Type': 'application/json;charset=UTF-8',
    'Referer': 'http://172.16.1.147:8000/',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'authorization': 'Basic ZWxhc3RpYzoxMjM0NTY=',
}

for i in range (150):
    num1 = random.randint(1, 9)
    num2 = random.randint(10, 99)
    name = random.randint(1001, 1150)
    if num1 in (1, 2, 3):
        name = "高密度场景"
    data = f'{{"id":"","region":"63883286","regionName":"test150+","name":"{name}","url":"vas://name=name&psw=psw&srvip=127.0.0.1&srvport=9080&devid=4301000000000100{num1}0{num2}&","category":1,"status":1,"location":"","direction":"","longitude":112.975831844401{num1}2,"latitude":28.1978107866521{num2}}}'

    response = requests.post('http://172.16.1.147:8000/u2s2/u2s/onlineCameraManager/addOnlineCamera', headers=headers, data=data.encode("utf-8"), verify=False)
    print(response.request.header)
# excel_zip = "excel.zip"
# dirs = r'D:/export_test/'
# if not os.path.exists(dirs):
#     os.makedirs(dirs)
# f = open(dirs + excel_zip, "wb")
# for chunk in response.iter_content(chunk_size=512):
#     if chunk:
#         f.write(chunk)

if __name__ == '__main__':
    pass



