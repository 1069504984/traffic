# -*- coding: utf-8 -*-
# @Time    : 2020/11/26 16:25
# @Author  : Fighter
import json
import random
import uuid
from locust import TaskSequence, HttpLocust, task, seq_task, between
from locust.contrib.fasthttp import FastHttpLocust
import base64
import requests
import os


class TestSuite(TaskSequence):
    def on_start(self):
        """
        初始化方法，相当于 __init__ 函数，或setup
        每次测试执行时，都会首先执行的  函数
        不需要 装饰器 定义

        """
        self.httpurl = "http://172.16.1.133:5555/u2s"
        self.header = {
            'Connection': 'keep-alive',
            'Accept': '*/*',
            'RequestRouting': '/target_retrieval',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36',
            'Authorization': 'eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJ7XCJzeXNSb2xlXCI6e1wicm9sZUlkXCI6MSxcInJvbGVOYW1lXCI6XCLns7vnu5_nrqHnkIblkZhcIixcInJvbGVSZW1hcmtcIjpcIueuoeeQhuWRmFwiLFwicm9sZVNpZ25cIjpcImFkbWluXCIsXCJzdGF0ZVwiOjF9LFwidXNlckRlcHRcIjp7XCJkZXB0SWRcIjoyMixcImRlcHRMZXZlbFwiOjEsXCJkZXB0TmFtZVwiOlwi6ZW_5rKZ5biC5YWs5a6J5bGAXCIsXCJkZXB0TnVtYmVyXCI6XCI0MzAxMDAwMDAwMDBcIixcImRlcHRTdGF0ZVwiOjEsXCJkaXNwbGF5TmFtZVwiOlwi6ZW_5rKZ5biC5YWs5a6J5bGAXCIsXCJpc0xlYWZcIjowLFwibG9uZ051bWJlclwiOlwiNDMwMTAwMDAwMDAwXCJ9LFwic3lzVXNlclwiOntcImNyZWF0ZVRpbWVcIjoxNjA5MzEwNTM5MDAwLFwiY3JlYXRlVXNlcklkXCI6MSxcImNyZWF0ZVVzZXJOYW1lXCI6XCLns7vnu5_nrqHnkIblkZhcIixcImRlcHRJZFwiOlwiNDMwMTAwMDAwMDAwXCIsXCJkaXNwb3NpdGlvbkFwcHJvdmFsXCI6MSxcImdyb3VwSWRcIjo0MzAxMDAwMDAwMDAsXCJpZE51bWJlclwiOlwiNDMwMTI0MTk5NjAzMDUwMDEzXCIsXCJpc0RlcHRBZG1pblwiOlwiMVwiLFwiaXN2YWxpZFwiOlwiMVwiLFwicGFzc3dvcmRcIjpcImU1MjMxMzM0MjgzYWI1NzQ4Mjc2MjNkZjA0NGUyYTk3XCIsXCJyZWFsTmFtZVwiOlwibGtcIixcInJlbWFya1wiOlwiXCIsXCJ0ZWxcIjpcIlwiLFwidXNlcklkXCI6MTYwOTMxMDUzODc1MCxcInVzZXJuYW1lXCI6XCJsa1wifX0iLCJpc3MiOiJpc3N1ZXIiLCJkZXB0TnVtIjoiNDMwMTAwMDAwMDAwIiwidXNlck5hbWUiOiJhZG1pbiIsImV4cCI6MTYxMDA4NjY5NSwidXNlcklkIjoiMSIsImlhdCI6MTYxMDAwMDI5NSwianRpIjoiNzk2NzQ0NTE3MzQzNTEwNTI4In0.TMWyfgSqbuA_kGG6KNspjcwUFdTgIAzDdvTnKxGRZ98',
            'Origin': 'http://172.16.1.133:8088',
            'Referer': 'http://172.16.1.133:8088/',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Access-Control-Request-Method': 'GET',
            'Access-Control-Request-Headers': 'authorization,requestrouting',
            'Sec-Fetch-Mode': 'cors',
            'Content-Type': 'application/json;charset=UTF-8',
        }
        self.cookie = {
            'SESSION': 'MzE1ZDczNDktNWQ0Ny00NWIzLWFmZDEtYWEzZjZlYmE0YjMz',
        }

    def on_stop(self):
        """
        测试执行结束后，执行的方法， 相当于teardown
        不需要用  装饰器 定义
        :return:
        """
        pass

    @task  # 装饰器，说明下面是一个测试任务
    @seq_task(1)  # 装饰器 说明任务的执行顺序
    def getTargetSearchList(self):
        data = '{"pageNum2":1,"pageSize2":27,"startTime":"2021-01-07 00:00:00","endTime":"2021-01-07 23:59:59","timeSelect":"desc","type":1,"cameraId":"","age":"","angle":"","angle2":"","bag":"","bikeAge":"","bikeGenre":"","bikeSex":"","cap":"","carcolor":"","carlogo":"","coatStyle":"","glasses":"","handbag":"","helmet":"","helmetcolorStr":"","license":"","lowcolorStr":"","nation":"","passengersUpColorStr":"","respirator":"","sex":"","taskTypeCode":"","trousersStyle":"","umbrella":"","upcolorStr":"","vehiclekind":"","vehicleseries":"","wheels":"","hairStyle":"","trolley":"","coatTexture":"","trousersTexture":"","objType":1,"gender":"","eyeglass":"","mouthmask":"","upperColor":"","upperStyle":"","upperTexture":"","lowerColor":"","lowerStyle":"","backpack":"","view":"","hair":"","shape":"","bicycleTricycle":"","subBicycleTricycle":"","bikeHasPlate":"","helmetColor":"","cartype":"","carColor":"","ptype":"","pcolor":"","vehicleBrand":"","vehicleSeries":"","rows":27,"page":1}'
        response = self.client.post(self.httpurl + "/targetSearch/getTargetSearchList", headers=self.header, data=data,
                                    catch_response=True, name='getTargetSearchList')
        try:
            if 0 == response.json().get("code"):
                response.success()
                print("目标检索: ",response.json())
            else:
                response.failure("目标检索查询失败")
                print("getTargetSearchList接口的返回值: "+str(response.json()))
        except Exception as e:
            print(e)


    # @task
    # @seq_task(2)
    # def initObjextResult(self):
    #     header = {
    #         'Connection': 'keep-alive',
    #         'Accept': 'application/json, text/plain, */*',
    #         'RequestRouting': '/image_search',
    #         'Authorization': 'eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJ7XCJzeXNSb2xlXCI6e1wicm9sZUlkXCI6MSxcInJvbGVOYW1lXCI6XCLns7vnu5_nrqHnkIblkZhcIixcInJvbGVSZW1hcmtcIjpcIueuoeeQhuWRmFwiLFwicm9sZVNpZ25cIjpcImFkbWluXCIsXCJzdGF0ZVwiOjF9LFwidXNlckRlcHRcIjp7XCJkZXB0SWRcIjoyMixcImRlcHRMZXZlbFwiOjEsXCJkZXB0TmFtZVwiOlwi6ZW_5rKZ5biC5YWs5a6J5bGAXCIsXCJkZXB0TnVtYmVyXCI6XCI0MzAxMDAwMDAwMDBcIixcImRlcHRTdGF0ZVwiOjEsXCJkaXNwbGF5TmFtZVwiOlwi6ZW_5rKZ5biC5YWs5a6J5bGAXCIsXCJpc0xlYWZcIjowLFwibG9uZ051bWJlclwiOlwiNDMwMTAwMDAwMDAwXCJ9LFwic3lzVXNlclwiOntcImRlcHRJZFwiOlwiNDMwMTAwMDAwMDAwXCIsXCJncm91cElkXCI6NDMwMTAwMDAwMDAwLFwiaXNEZXB0QWRtaW5cIjpcIjFcIixcImlzdmFsaWRcIjpcIjFcIixcInBhc3N3b3JkXCI6XCI4ODU3NjZhMTNlOTVlNjA5ZGQ2YTRiZjY2ZWNhZWJlM1wiLFwicmVhbE5hbWVcIjpcIuezu-e7n-euoeeQhuWRmFwiLFwidGVsXCI6XCIxMzc1NTE1OTA4MlwiLFwidXNlcklkXCI6MSxcInVzZXJuYW1lXCI6XCJhZG1pblwifX0iLCJpc3MiOiJpc3N1ZXIiLCJkZXB0TnVtIjoiNDMwMTAwMDAwMDAwIiwidXNlck5hbWUiOiJhZG1pbiIsImV4cCI6MTYwODEyMTY3NSwidXNlcklkIjoiMSIsImlhdCI6MTYwODAzNTI3NSwianRpIjoiNzg4NTAyNjI1OTI1NDY0MDY0In0.lilCP8FszryuV9x5eax0ovwus_-5imnLvgVj64zo5JE',
    #         'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36',
    #         'Content-Type': 'application/x-www-form-urlencoded',
    #         'Origin': 'http://172.16.1.147:8088',
    #         'Referer': 'http://172.16.1.147:8088/',
    #         'Accept-Language': 'zh-CN,zh;q=0.9',
    #     }
    #     response = self.client.post(self.httpurl + "/twiceImageQuery/initObjextResult/page=1&rows=12&objtype=1&startTime=2020-12-16+00%3A00%3A00&endTime=2020-12-16+23%3A59%3A59", headers=header,
    #                                 )
    #
    #     if 0 == response.json().get("code"):
    #         response.success()
    #
    #     else:
    #         response.failure("初始化以图搜图查询失败")
    #         print(response.json())

    @task  # 装饰器，说明下面是一个测试任务
    @seq_task(2)  # 装饰器 说明任务的执行顺序
    def searchBySerialNumber(self):
        data = '{"pageNo":1,"pageSize":24,"type":"","order":"desc","objextType":"","serialNumber":"202101051458080043511024","insertTimeStart":"2021-01-03 14:57:31","insertTimeEnd":"2021-01-05 14:57:31","analysisTypes":"1,2,3,4","cameraFileId":"1603854940113","taskType":3}'
        response = self.client.post("http://172.16.1.133:5555/video/u2sTask/searchBySerialNumber", headers=self.header,
                                    data=data,
                                    catch_response=True, name='searchBySerialNumber')
        try:
            if response.json().get("state") == True:
                response.success()
                print("单任务查询",response.json())
            else:
                response.failure("单任务查询目标失败")
                print("searchBySerialNumber接口的返回值:" + str(response.json()))
        except Exception as e:
            print("异常:"+e)



class WebsiteUser(FastHttpLocust):
    task_set = TestSuite  # 指定测试套件    task_set 固定
    wait_time = between(0, 1)  # 定义执行过程中随机等待时间区间，单位 秒
    host = 'http://172.16.1.133:5555'


if __name__ == '__main__':
    host = "127.0.0.1"
    os.system(f"locust -f test_qurey.py --web-host={host}")
