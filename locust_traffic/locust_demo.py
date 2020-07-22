# -*- coding: utf-8 -*-
# @Time    : 2020/4/16 19:31
# @Author  : Fighter
import base64
from common.utils import get_base64
import requests, time, json, threading, random
# !/usr/bin/env python
# -*- coding:utf-8 -*-

import requests, time, json, threading, random


class Presstest(object):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36',
        'Content-Type': 'application/json; charset=UTF-8',
    }

    def __init__(self, press_url, pictureurl):
        self.pictureurl = pictureurl
        self.press_url = press_url
        self.session = requests.Session()
        self.session.headers = self.headers

    def testinterface(self):
        '''压测接口'''
        data = get_base64(self.pictureurl)
        global ERROR_NUM
        try:
            html = self.session.post(self.press_url, data=data)
            if html.json().get('StatusString') != 'OK':
                print(html.json())
                ERROR_NUM += 1
        except Exception as e:
            print(e)
            ERROR_NUM += 1

    def testonework(self):
        '''一次并发处理单个任务'''
        i = 0
        while i < ONE_WORKER_NUM:
            i += 1
            self.testinterface()
        time.sleep(LOOP_SLEEP)

    def run(self):
        '''使用多线程进程并发测试'''
        t1 = time.time()
        Threads = []

        for i in range(THREAD_NUM):
            t = threading.Thread(target=self.testonework, name="T" + str(i))
            t.setDaemon(True)
            Threads.append(t)

        for t in Threads:
            t.start()
        for t in Threads:
            t.join()
        t2 = time.time()

        print("===============压测结果===================")
        print("URL:", self.press_url)
        print("任务数量:", THREAD_NUM, "*", ONE_WORKER_NUM, "=", THREAD_NUM * ONE_WORKER_NUM)
        print("总耗时(秒):", t2 - t1)
        print("每次请求耗时(秒):", (t2 - t1) / (THREAD_NUM * ONE_WORKER_NUM))
        print("每秒承载请求数:", 1 / ((t2 - t1) / (THREAD_NUM * ONE_WORKER_NUM)))
        print("错误数量:", ERROR_NUM)


if __name__ == '__main__':
    press_url = 'http://172.16.1.118:9999/VIID/Images/'
    data = '/Data'
    url1 = random.randint(1, 10000)
    new_url = press_url + str(url1) + data
    url = r'D:\副驾驶安全带（有）-100张\TIM截图20190521162551.jpg'

    THREAD_NUM = 20  # 并发线程总数
    ONE_WORKER_NUM = 1  # 每个线程的循环次数
    LOOP_SLEEP = 0  # 每次请求时间间隔(秒)
    ERROR_NUM = 0  # 出错数

    obj = Presstest(press_url=new_url, pictureurl=url)
    obj.run()
