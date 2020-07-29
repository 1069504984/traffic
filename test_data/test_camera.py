# -*- coding: utf-8 -*-
# @Time    : 2020/1/21 16:45
# @Author  : Fighter
from common.do_mysql import DoMysql
import unittest
from common import get_data
from common.do_requests import DoRequests
from common.learn_do_excel import DoExcel
from common import project_path
from common.my_log import MyLogg
from common.do_yaml import do_conf_yaml
import requests
import json
import warnings
import allure
import pytest
import os
import logging
my_log = MyLogg()
sheet_name = "camera"
test_data = DoExcel(project_path.test_case_path, sheet_name).read_data()



@allure.feature("监控点")
class TestCases():

    @pytest.fixture()
    def setUp0(self):  # 测试之前的准备工作
        warnings.simplefilter("ignore", ResourceWarning)

    @pytest.fixture()
    def setup1(self):
        self.do_request = DoRequests()
        self.do_request.add_headers(do_conf_yaml.read("api", "authorization"))

    def tearDown(self):
        pass

    def analysis_check(self, expected, api_check, response):
        if api_check == []:
            my_log.my_info("此用例暂无深度检查点---------进行浅度检查")
            if "code" in response:
                assert expected["code"] == response["code"]
            elif "state" in response:
                assert expected["state"] == response["state"]
        if len(api_check) == 1:
            left_param = api_check.split("==")[0]
            right_param = api_check.spilt("==")[1]
            if right_param in response.keys():
                assert expected.get(right_param) == response.get(right_param)
            else:
                my_log.my_error(F"key: {right_param} --不存在，请check返回值")
        elif len(api_check) > 1:
            for j in api_check:
                left_param = j.split("==")[0]
                right_param = j.split("==")[1]
                if right_param in response.keys():
                    assert expected.get(right_param) == response.get(right_param)
                else:
                    my_log.my_error(F"key: {right_param} --不存在，请check返回值")

    def extra_check(self, item):
        check_ponit = item["check"]
        if check_ponit is not None:
            check_ponit_list = check_ponit.split("\n")
            for index, check in enumerate(check_ponit_list):
                if check == "":
                    del check_ponit_list[index]
        else:
            check_ponit_list = []
        return check_ponit_list


    @pytest.mark.parametrize('item', test_data)
    @pytest.mark.usefixtures("setup1")
    def test_001(self, item, setUp0):
        '''
        监控点接口
        '''
        global result  # 指明全球变量
        global COOKIES  # 设置cookies为全局变量

        allure.dynamic.title(item['title'])
        allure.dynamic.description(item['title'])
        # 获取item中的用例数据
        url = item["url"]
        url = get_data.GetData().replace(url)
        method = item["method"]
        param = item["param"]  # 返回的是字符串类型的数据
        case_id = item["case_id"]
        modular = item["modular"]
        title = item["title"]
        expected = item["expected"]
        check_ponit_list = self.extra_check(item)
        header = eval(item["header"])

        self.do_request.add_headers(do_conf_yaml.read("api", "authorization"))  # 添加认证信息
        extra_token = getattr(get_data.GetData, "token")
        token_header = {'keensense-traffic-token': extra_token}
        self.do_request.add_headers(token_header)  # 添加token
        self.do_request.add_headers(header)  # 添加原始头部

        sql = item["sql"]
        print(sql)
        param = get_data.GetData().replace(param)
        print("最终param-----{}".format(param))
        if sql is not None:
            sql = get_data.GetData().replace(sql)
            print("最终sql------{}".format(sql))
        my_log.my_info("正在发起{}模块中的第{}条用例:{}".format(modular, case_id, title))
        my_log.my_info("测试数据是：{}".format(param))
        test_result = DoRequests.be_result(item, param, url, method, self.do_request.session.headers)  # 发起请求
        print(test_result.text)
        if getattr(get_data.GetData, 'cameraId') is not None:
            print("删除的camemaId:{}".format(getattr(get_data.GetData, 'cameraId')))
        # 增加一个判断 是在完成完请求之后才去判断
        # 获取cameraId
        if sql is not None and eval(sql)["sql_1"]:
            delete_cameraId = DoMysql().do_mysql(eval(sql)["sql_1"], 1)
            if delete_cameraId is None:
                my_log.my_info("监控点删除成功")
            else:
                cameraId = DoMysql().do_mysql(eval(sql)["sql_1"], 1)[0]
                setattr(get_data.GetData, 'cameraId', str(cameraId))

        if test_result.cookies:  # 判断请求cookies是否为空
            cookies = requests.utils.dict_from_cookiejar(test_result.cookies)
            setattr(get_data.GetData, "COOKIES", cookies)
        if title == "登录接口正常验证":  # 提取token
            if test_result.json().get("data"):
                token = test_result.json().get("data")
                setattr(get_data.GetData, "token", token)
        new_expected = json.loads(expected)  # 处理Null无法识别的问题
        # 输出测试结果和实际结果，进行断言比对，注意这里需要将实际结果的数据和预期结果的数据都改成字典类型，方便比对
        my_log.my_info("测试结果：{}".format(test_result.json()))
        my_log.my_info("预期结果：{}".format(new_expected))
        try:
            # assert new_expected.get(check[0]) == test_result.json().get(check[0])
            self.analysis_check(new_expected, check_ponit_list, test_result.json())
            result = "pass"
            my_log.my_info("测试通过")
        except AssertionError as e:
            my_log.my_error("测试失败，断言错误")
            result = "failed"
            my_log.my_error(
                F"请检查请求参数------------------- param:{param}\n url: {url}\n method: {method}\n header: {self.do_request.session.headers}")
            raise e
        finally:
            row = case_id + 1
            # 这里需要注意写回测试数据的时候，需要把测试数据转换成字符串类型
            DoExcel(project_path.test_case_path, sheet_name).write_data(row, test_result.text, result)


if __name__ == '__main__':
    pytest.main(["-s", "--alluredir", "./allure", '--clean-alluredir', 'test_camera.py'])
    os.system("allure generate ./allure -o ./allure/html -c")
