# -*- coding: utf-8 -*-
# @Time    : 2020/8/5 13:49
# @Author  : Fighter
import json
import random
import uuid
from locust import TaskSequence, HttpLocust, task, seq_task, between
from locust.contrib.fasthttp import FastHttpLocust


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
        self.uuid = str(uuid.uuid4())
        # self.headers = {"Content-Type": "application/json"}
        self.objext_type = 3

        self.httpurl = "http://172.16.1.138:6091/rebalance/message"
        self.big_img = "http://172.16.1.138:8891/group1/M00/04/F9/rBABil9W4smAfL70AAHBJjtI2Rc613.jpg"
        self.frame_img = "/home/jiuling/img/face.jpg"


    def on_stop(self):
        """
        测试执行结束后，执行的方法， 相当于teardown
        不需要用  装饰器 定义
        :return:
        """
        pass

    @task  # 装饰器，说明下面是一个测试任务
    @seq_task(1)  # 装饰器 说明任务的执行顺序
    def test_massage(self):
        url = '/rebalance/message'
        data = {
            "pic_roi": [32, 24, 89, 108],
            "picture_type": 1,
            "leave_time": "20200908000205",
            "big_img": self.big_img,
            "frame_img": self.frame_img,
            "device_id": "1234567891011",
            "serial_number": "1544005441",
            "ext_info": {
                "EndFramePts": 125560,
                "StartFramePts": 120760,
                "LeftTopY": 552,
                "LeftTopX": 1664,
                "FramePts": 125320,
                "EndFrameIdx": 3138,
                "StartFrameIdx": 3018,
                "ObjId": 190,
                "AnalysisId": 1544005441,
                "RightBtmY": 816,
                "Height": 1080,
                "RightBtmX": 1806,
                "FrameIdx": 3132,
                "Width": 1920
            },
            "enter_time": "20200909000205",
            "uuid": str(uuid.uuid4()),
            "objext_type": self.objext_type,
            "capture_time": "20200909000200"
        }
        str_data = json.dumps(data)
        # self.client 发起请求，相当于requests
        # catch_response 值为True 允许为失败 ， name 设置任务标签名称   -----可选参数
        rsp = self.client.post(url, data=str_data, catch_response=True, name='test_massage')
        # 进行结果断言
        if int(rsp.text) == 1:
            rsp.success()
            print(rsp.text)
            #print(self.uuid)
        else:
            rsp.failure("消息发送失败")
            print(rsp.text)
        # 结果断言的方式还可以： rsp.ok 返回True则说明响应状态小于400

    # @task
    # @seq_task(2)
    # def login_case(self):
    #     url = '/erp/loginIn'
    #     data = {"name": self.user, "pwd": self.pwd}
    #     rsp = self.client.post(url, json=data, headers=self.headers, catch_response=True, name='test_1')
    #     self.token = rsp.json()['token']  # 提取响应信息中的 token
    #     print(self.token)
    #     if rsp.status_code == 200:
    #         rsp.success()
    #     else:
    #         rsp.failure("login登录失败")
    #
    # @task
    # @seq_task(3)
    # def getuser_case(self):
    #     url = '/erp/user'
    #     headers = {"Token": self.token}
    #     rsp = self.client.get(url, headers=headers, catch_response=True, name='test_2')
    #     if rsp.status_code == 200:
    #         rsp.success()
    #     else:
    #         rsp.failure("getuser获取用户失败")


class RunCase(FastHttpLocust):
    """
    创建 压测类 继承 HttpLocust
    """
    task_set = TestSuite  # 指定测试套件    task_set 固定
    wait_time = between(0, 1)  # 定义执行过程中随机等待时间区间，单位 秒
    host = 'http://172.56.1.227:6091'



