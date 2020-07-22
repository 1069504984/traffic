# -*- coding: utf-8 -*-
# @Time    : 2019/12/10 16:16
# @Author  : Fighter
import requests
import os

cookies = {
    'JSESSIONID': 'e2aa441c-041e-45a0-9320-e5659352315a',
}

headers = {
    'Connection': 'keep-alive',
    'Origin': 'http://172.16.1.107:9088',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36',
    'Content-Type': 'application/json',
    'Accept': '*/*',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.9',
}

data = '{"commonReq":{"cameraIdList":[],"ctrlUnitFileIdList":[],"endTime":"2020-04-26 23:06:00","order":"asc","pageNo":1,"pageSize":5,"startTime":"2020-04-26 23:00:00","serialnumber":"","objType":"2"}}'

response = requests.post('http://172.16.1.107:9088/objext/download', headers=headers, cookies=cookies, data=data,
                         verify=False)
print(response.status_code)
excel_zip = "excel.zip"
dirs = r'D:/export_test/'
if not os.path.exists(dirs):
    os.makedirs(dirs)
f = open(dirs + excel_zip, "wb")
for chunk in response.iter_content(chunk_size=512):
    if chunk:
        f.write(chunk)
