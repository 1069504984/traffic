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
    import os

    # master 启动
    # os.system(" locust -f  demo2.py  --host=https://www.cnblogs.com")
    # slave 启动
    os.system("locust -f demo2.py --web-host='127.0.0.1'")
