# -*- coding: utf-8 -*-
# @Time    : 2020/8/5 13:49
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
    """
    创建一个测试用例管理类，继承 带有顺序的类TaskSequence
    """

    def on_start(self):
        """
        初始化方法，相当于 __init__ 函数，或setup
        每次测试执行时，都会首先执行的  函数
        不需要 装饰器 定义

        """
        self.path = r'E:/项目/交通/bike/'  # 图像读取地址
        self.filelist = os.listdir(self.path)  # 打开对应的文件夹
        self.total_num = len(self.filelist)  # 得到文件夹中图像的个数

          # 拼接图像的读取地址
            # 对图像数据类型进行转换

    def on_stop(self):
        """
        测试执行结束后，执行的方法， 相当于teardown
        不需要用  装饰器 定义
        :return:
        """
        pass

    @task  # 装饰器，说明下面是一个测试任务
    @seq_task(1)  # 装饰器 说明任务的执行顺序
    def post_image(self):
        for i in range(self.total_num):
            jpg_name = self.path + str(i + 1) + '.jpg'
            with open(jpg_name, 'rb') as f:
                image = f.read()
                image_base64 = str(base64.b64encode(image), encoding='utf-8')
                data_image = 'data:image/jpeg;base64,' + image_base64
                body = {
                    "scenes": 4,
                    "isDetectFullFrame": 1,
                    "images":
                        [
                            {
                                "id": "1001",
                                "data": data_image
                            },{
                                "id": "1002",
                                "data": data_image
                            },{
                                "id": "1003",
                                "data": data_image
                            },{
                                "id": "1004",
                                "data": data_image
                            },{
                                "id": "1005",
                                "data": data_image
                            },{
                                "id": "1006",
                                "data": data_image
                            },{
                                "id": "1007",
                                "data": data_image
                            },{
                                "id": "1008",
                                "data": data_image
                            },{
                                "id": "1009",
                                "data": data_image
                            },{
                                "id": "1010",
                                "data": data_image
                            }
                    ]
                }
                data = json.dumps(body)

                headers = {'Content-Type': 'application/json'}
                url = '/v8/images/objects'
                response=self.client.post(url, headers=headers, data=data, catch_response=True, name='test_bike')
                if response:
                    response.success()
                else:
                    response.failure()




class RunCase(FastHttpLocust):
    """
    创建 压测类 继承 HttpLocust
    """
    task_set = TestSuite  # 指定测试套件    task_set 固定
    wait_time = between(0, 1)  # 定义执行过程中随机等待时间区间，单位 秒
    host ="http://172.16.1.76:8100"

