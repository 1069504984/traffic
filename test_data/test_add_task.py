# -*- coding: utf-8 -*-
# @Time    : 2020/1/21 16:45
# @Author  : Fighter
import os

import allure
import pytest
from common.do_mysql import DoMysql
from common import get_data
from common.do_requests import DoRequests
from common.learn_do_excel import DoExcel
from common import project_path
from common.my_log import MyLogg
import requests
import json
import warnings
import time

my_log = MyLogg()
test_data = DoExcel(project_path.test_case_path, "add_task").read_data()
video_data = DoExcel(project_path.test_case_path, "video").read_data()[2]


@pytest.fixture()
def setUp():  # 测试之前的准备工作
    warnings.simplefilter("ignore", ResourceWarning)
    print('休眠0.5秒')
    time.sleep(0.5)


@allure.feature("结构化任务添加")
class TestCases():

    @pytest.mark.parametrize('item', test_data)
    def test_001(self, item, setUp):
        '''
        任务模块接口流程用例
        '''
        global result
        global COOKIES
        allure.dynamic.title(item['title'])
        allure.dynamic.description(item['title'])
        # 获取item中的用例数据
        url = item["url"]
        url = get_data.GetData().replace(url)
        method = item["method"]
        param = item["param"]  # 返回的是字符串类型的数据
        case_id = item["case_id"]
        modular = item["modular"]
        header = eval(item["header"])
        title = item["title"]
        if title == "添加结构化任务":
            qurey_cameraid = "SELECT id FROM u2s_traffic.camera WHERE name='测试test'"
            cameraid = DoMysql().do_mysql(qurey_cameraid)[0]
            url = video_data["url"]
            param = str(eval(video_data["param"])[0])
            param = get_data.GetData().replace(param)
            param = eval(param)
            files = eval(video_data["param"])[-1]
            header = eval(video_data["header"])
            test_result = DoRequests(url, method, param, files=files).request(headers=header,
                                                                              cookies=getattr(get_data.GetData,
                                                                                              "COOKIES"))

            qurey_fileid = "SELECT id FROM u2s_traffic.ctrl_unit_file WHERE camera_id={}".format(cameraid)
            fileid = DoMysql().do_mysql(qurey_fileid)[0]
            setattr(get_data.GetData, "cameraFileId", str(fileid))
            setattr(get_data.GetData, "cameraId", str(cameraid))
            time.sleep(15)

        expected = item["expected"]
        param = item["param"]
        url = item["url"]
        url = get_data.GetData().replace(url)
        sql = item["sql"]
        if sql is not None:
            sql = get_data.GetData().replace(sql)
            print("从数据库获取的参数化sql:{}".format(sql))
        param = get_data.GetData().replace(param)
        print("目前的param是{}".format(param))
        my_log.my_info("正在发起{}模块中的第{}条用例:{}".format(modular, case_id, title))
        my_log.my_info("测试数据是：{}".format(param))
        # 执行接口测试，cookies利用反射进行动态的获取

        if "application/json" in item["header"]:
            new_param = param
        else:
            new_param = eval(param)
        if isinstance(new_param, tuple):
            test_result = DoRequests(url, method, new_param).request(headers=header,
                                                                     cookies=getattr(get_data.GetData, "COOKIES"))
        else:

            test_result = DoRequests(url, method, new_param.encode("utf-8")).request(headers=header,
                                                                                     cookies=getattr(get_data.GetData,
                                                                                                     "COOKIES"))
        if "data" in test_result.json() and test_result.json()["data"] is not None and len(
                test_result.json()["data"]) == 19:
            setattr(get_data.GetData, "serialnumber", test_result.json()["data"])
            print("需要删除的任务号为:{}".format(getattr(get_data.GetData, "serialnumber")))
        print(test_result.text)

        # 增加一个判断 是在完成完请求之后才去判断
        # 获取cameraId
        if sql is not None and "sql_1" in eval(sql):
            delete_cameraId = DoMysql().do_mysql(eval(sql)["sql_1"], 1)
            if delete_cameraId is None:
                my_log.my_info("监控点删除成功")
            else:
                cameraId = DoMysql().do_mysql(eval(sql)["sql_1"], 1)[0]
                setattr(get_data.GetData, 'cameraId', str(cameraId))
                print("需要删除的camemaId:{}".format(getattr(get_data.GetData, 'cameraId')))
        # 获取任务号
        if sql is not None and "sql_2" in eval(sql):
            task_data = DoMysql().do_mysql(eval(sql)["sql_2"], 1)
            print(task_data)
            my_log.my_info("新增任务获取的任务号数据为{}".format(task_data))

        if test_result.cookies:  # 判断请求cookies是否为空
            cookies = requests.utils.dict_from_cookiejar(test_result.cookies)
            setattr(get_data.GetData, "COOKIES", cookies)
        new_expected = json.loads(expected)  # 处理Null无法识别的问题
        # 输出测试结果和实际结果，进行断言比对，注意这里需要将实际结果的数据和预期结果的数据都改成字典类型，方便比对
        my_log.my_info("测试结果是：{}".format(test_result.json()))
        my_log.my_info("预期结果是：{}".format(new_expected))
        try:
            if "code" in test_result.json():
                assert new_expected["code"] == test_result.json()["code"]
                result = "pass"
                my_log.my_info("测试通过了")
            elif "state" in test_result.json():
                assert new_expected["state"] == test_result.json()["state"]
                result = "pass"
                my_log.my_info("测试通过了")
        except AssertionError as e:
            my_log.my_error("测试失败，断言错误")
            result = "failed"
            raise e
        finally:
            row = case_id + 1
            # 这里需要注意写回测试数据的时候，需要把测试数据转换成字符串类型
            DoExcel(project_path.test_case_path, "add_task").write_data(row, test_result.text, result)


if __name__ == '__main__':
    pytest.main(["-s", "--alluredir", "./allure", '--clean-alluredir', 'test_add_task.py'])
    os.system("allure generate ./allure -o ./allure/html -c")
