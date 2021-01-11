# -*- coding: utf-8 -*-
# @Time    : 2020/4/16 19:31
# @Author  : Fighter
import json
import random
from http import client

import requests


def searchBySerialNumber():
    num = 0
    err_num = 0
    for i in range(100):
        header = {
            'Connection': 'keep-alive',
            'Accept': '*/*',
            'RequestRouting': '/taskMgt',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36',
            'Authorization': 'eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJ7XCJzeXNSb2xlXCI6e1wicm9sZUlkXCI6MSxcInJvbGVOYW1lXCI6XCLns7vnu5_nrqHnkIblkZhcIixcInJvbGVSZW1hcmtcIjpcIueuoeeQhuWRmFwiLFwicm9sZVNpZ25cIjpcImFkbWluXCIsXCJzdGF0ZVwiOjF9LFwidXNlckRlcHRcIjp7XCJkZXB0SWRcIjoyMixcImRlcHRMZXZlbFwiOjEsXCJkZXB0TmFtZVwiOlwi6ZW_5rKZ5biC5YWs5a6J5bGAXCIsXCJkZXB0TnVtYmVyXCI6XCI0MzAxMDAwMDAwMDBcIixcImRlcHRTdGF0ZVwiOjEsXCJkaXNwbGF5TmFtZVwiOlwi6ZW_5rKZ5biC5YWs5a6J5bGAXCIsXCJpc0xlYWZcIjowLFwibG9uZ051bWJlclwiOlwiNDMwMTAwMDAwMDAwXCJ9LFwic3lzVXNlclwiOntcImRlcHRJZFwiOlwiNDMwMTAwMDAwMDAwXCIsXCJncm91cElkXCI6NDMwMTAwMDAwMDAwLFwiaXNEZXB0QWRtaW5cIjpcIjFcIixcImlzdmFsaWRcIjpcIjFcIixcInBhc3N3b3JkXCI6XCI4ODU3NjZhMTNlOTVlNjA5ZGQ2YTRiZjY2ZWNhZWJlM1wiLFwicmVhbE5hbWVcIjpcIuezu-e7n-euoeeQhuWRmFwiLFwidGVsXCI6XCIxMzc1NTE1OTA4MlwiLFwidXNlcklkXCI6MSxcInVzZXJuYW1lXCI6XCJhZG1pblwifX0iLCJpc3MiOiJpc3N1ZXIiLCJkZXB0TnVtIjoiNDMwMTAwMDAwMDAwIiwidXNlck5hbWUiOiJhZG1pbiIsImV4cCI6MTYwODEyMTY3NSwidXNlcklkIjoiMSIsImlhdCI6MTYwODAzNTI3NSwianRpIjoiNzg4NTAyNjI1OTI1NDY0MDY0In0.lilCP8FszryuV9x5eax0ovwus_-5imnLvgVj64zo5JE',
            'Origin': 'http://172.16.1.147:8088',
            'Referer': 'http://172.16.1.147:8088/',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Access-Control-Request-Method': 'GET',
            'Access-Control-Request-Headers': 'authorization,requestrouting',
            'Sec-Fetch-Mode': 'cors',
            'Content-Type': 'application/json;charset=UTF-8',
        }
        cookie = {
            'SESSION': 'MzE1ZDczNDktNWQ0Ny00NWIzLWFmZDEtYWEzZjZlYmE0YjMz',
        }
        data = '{"pageNo":1,"pageSize":24,"type":"","order":"desc","objextType":"","serialNumber":"1608036065319","insertTimeStart":"2020-12-15 09:43:49","insertTimeEnd":"2020-12-16 09:43:49","analysisTypes":"1,2,3,4","cameraFileId":"100404","taskType":3}'
        response = requests.post("http://172.16.1.147:5555/video/u2sTask/searchBySerialNumber", headers=header,
                                    data=data,
                                    cookies=cookie,
                                    )
        num += 1
        try:
            if response.json().get("state") == True:
                print("成功")
            else:
                print("失败，state不为True")
                print(response.json())
                err_num += 1
        except Exception as e:
            print("异常:" + e)
            print("searchBySerialNumber接口的返回值:" + str(response.json()))
        else:
            print(f"searchBySerialNumber接口无异常次数{num},异常次数{err_num}")


if __name__ == '__main__':
    searchBySerialNumber()

