# -*- coding: utf-8 -*-
# @Time    : 2020/4/27 10:32
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
test_data = DoExcel(project_path.test_case_path, "online_video").read_data()


@pytest.fixture()
def setUp():  # 测试之前的准备工作
    warnings.simplefilter("ignore", ResourceWarning)
    print('休眠0.5秒')
    time.sleep(0.5)


@allure.feature("实时流添加")
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
        expected = item["expected"]
        sql = item["sql"]
        if sql is not None:
            sql = get_data.GetData().replace(sql)
            print("从数据库获取的参数化sql:{}".format(sql))
        param = get_data.GetData().replace(param)
        print("目前的param是{}".format(param))
        my_log.my_info("正在发起{}模块中的第{}条用例:{}".format(modular, case_id, title))
        if title == "删除实时流(批量)":
            time.sleep(5)
        elif "实时任务" in title:
            time.sleep(20)
        my_log.my_info("测试数据是：{}".format(param))
        test_result = DoRequests.be_result(item, param, url, method, header)
        number_json_extra = get_data.GetData.get_json_value(test_result.json(), "data")
        if number_json_extra is not False:
            my_log.my_warning(F"------正在建立关联数据----number_json_extra----{number_json_extra[0]}")
            if number_json_extra[0] is None:
                my_log.my_warning("关联数据不符合条件，正在剔除-------")
            elif len(number_json_extra[0]) < 18 or isinstance(number_json_extra[0], (dict, list)):
                my_log.my_warning("关联数据不符合条件，正在剔除-------")
            else:
                setattr(get_data.GetData, "serialnumber", number_json_extra[0])
            if eval(getattr(get_data.GetData, 'serialnumber')) is not 1111:
                print("需要删除的任务号为:{}".format(getattr(get_data.GetData, "serialnumber")))
        print(test_result.text)

        # 增加一个判断 是在完成完请求之后才去判断
        # 获取cameraId
        if sql is not None and "sql_1" in sql:
            delete_cameraId = DoMysql().do_mysql(eval(sql)["sql_1"], 1)
            if delete_cameraId is None:
                my_log.my_info("监控点删除成功")
            else:
                cameraId = DoMysql().do_mysql(eval(sql)["sql_1"], 1)[0]
                setattr(get_data.GetData, 'cameraId', str(cameraId))
                print("需要删除的camemaId:{}".format(getattr(get_data.GetData, 'cameraId')))
        # 获取任务号
        if sql is not None and "sql_2" in sql:
            task_data = DoMysql().do_mysql(eval(sql)["sql_2"], 1)
            if task_data is not None:
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
            assert new_expected["code"] == test_result.json()["code"]
            result = "pass"
            my_log.my_info("测试通过了")
        except AssertionError as e:
            my_log.my_error("测试失败，断言错误")
            result = "failed"
            raise e
        finally:
            row = case_id + 1
            # 这里需要注意写回测试数据的时候，需要把测试数据转换成字符串类型
            DoExcel(project_path.test_case_path, "online_video").write_data(row, test_result.text, result)


if __name__ == '__main__':
    pytest.main(["-s", "--alluredir", "./allure", '--clean-alluredir', 'test_online_video.py'])
    os.system("allure generate ./allure -o ./allure/html -c")
