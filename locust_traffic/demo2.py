# -*- coding: utf-8 -*-
# @Time    : 2020/7/24 14:46
# @Author  : Fighter
import random
from locust import HttpLocust, TaskSet, task, between


# 定义用户行为
class UserBehavior(TaskSet):
    def on_start(self):
        print("start")

    @task(1)
    def bky_index(self):
        self.client.get("/")

    @task(2)
    def blogs(self):
        self.client.get("/Clairewang/p/8622280.html")


class WebsiteUser(HttpLocust):
    host = "https://www.cnblogs.com"
    task_set = UserBehavior
    min_wait = 1500
    max_wait = 5000

    # # 等同于上面wait_time，单位毫秒
    # min_wait = 3000
    # max_wait = 6000


if __name__ == "__main__":
    # import os
    #     #
    #     # # master 启动
    #     # # os.system(" locust -f  demo2.py  --host=https://www.cnblogs.com")
    #     # # slave 启动
    #     # os.system("locust -f demo2.py --web-host='127.0.0.1'")
    header2 = {'Accept': '*/*',
               'Connection': 'keep-alive', }
    header = {'keensense-traffic-token': 1}
    header3 = {
        'Connection': 'keep-alive',
        'Accept': 'application/json, text/plain, */*',
        'Origin': 'http://172.16.1.107:9088',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36',
        'Content-Type': 'application/json;charset=UTF-8',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'authorization': 'Basic ZWxhc3RpYzoxMjM0NTY=',
    }
    # header2.update(header)
    header2.update(header3)
    print(header2)
    print(header2)
    header2.update(header)
    print(header2)
