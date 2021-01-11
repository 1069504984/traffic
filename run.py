import multiprocessing
import subprocess

from test_data.test_camera import TestCases
__author__ = '李开'
import pytest
import os

# 生成对应的测试报告
# import unittest
# import HTMLTestRunnerNew
#
# from test_data import task
# from test_data import test_camera
# import  os,sys
# from MakeReport import MakerReport
# curPath = os.path.abspath(os.path.dirname(__file__))
# rootPath = os.path.split(curPath)[0]
# sys.path.append(rootPath)
def run_dev(msg):
    os.system(msg)
if __name__ == '__main__':

    list=[r'pytest xxx1',r'pytest xxx2']
    pool = multiprocessing.Pool(processes=3)
    for i in range(2):
        msg = list[i]
        pool.apply_async(run_dev, (msg,))
    pool.close()
    pool.join()
    os.popen('allure xxxxxx')

    # os.system(r'pytest C:\Users\chens\Desktop\api_practise_1\test_data\test_camera.py --alluredir=allure')
    # pytest.main(["-s", "--alluredir", "./allure", '--clean-alluredir', './test_data/test_camera.py'])

    #     pytest.main(["-v", "--alluredir", "./allure/json", '--clean-alluredir'
    #                  ])
    #     os.system("allure generate ./allure/json -o ./allure/html -c")
    # #  './test_data/test_video.py',
    # # './test_data/test_camera.py',
    # #                  './test_data/test_query_task.py',
    # #                  './test_data/test_add_task.py'
    #

list=[r'pytest .\test_data\test_camera.py --alluredir=allure',
          r'pytest .\test_data\test_structuring.py --alluredir=allure']