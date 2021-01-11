# -*- coding: utf-8 -*-
# @Time    : 2020/1/21 16:45
# @Author  : Fighter
from common.do_mysql import DoMysql
from common import get_data
from common.do_requests import DoRequests
from common.learn_do_excel import DoExcel, extra_check
from common import project_path
from common.log_demo import logger
from common.do_yaml import do_conf_yaml
import requests
import json
import warnings
import allure
import pytest
import os
from utils.utils import Context
from multiprocessing import Process
# import logging
# logger = MyLogg()
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


    def analysis_check(self, api_check, response):
        a=Context()


    @pytest.mark.parametrize('item', test_data)
    @pytest.mark.usefixtures("setup1")
    def test_001(self, item, setUp0):
        '''
        监控点接口
        '''
        global result  # 指明全Ju变量
        global COOKIES  # 设置cookies为全局变量

        allure.dynamic.title(item['title'])
        allure.dynamic.description(item['title'])
        url,method,param,case_id,modular,title,expected,check_point_dict,header,extra=DoExcel.iter_excel_params(item)
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
        logger.info("正在发起{}模块中的第{}条用例:{}".format(modular, case_id, title))
        logger.info("测试数据是：{}".format(param))
        with allure.step("发起请求，获取实际结果"):
            test_result = DoRequests.be_result(item, param, url, method, self.do_request.session.headers)  # 发起请求
            try:
                if isinstance(json.loads(test_result.text), dict):
                    print(test_result.text)
            except Exception as e:
                print("返回内容不是Json格式，请检查请求参数"+"*"*20 + "\n" + str(test_result.url))
        if getattr(get_data.GetData, 'cameraId') is not None:
            print("删除的camemaId:{}".format(getattr(get_data.GetData, 'cameraId')))
        # 增加一个判断 是在完成完请求之后才去判断
        # 获取cameraId
        if sql is not None and eval(sql)["sql_1"]:
            delete_cameraId = DoMysql().do_mysql(eval(sql)["sql_1"], 1)
            if delete_cameraId is None:
                logger.info("监控点删除成功")
            else:
                cameraId = DoMysql().do_mysql(eval(sql)["sql_1"], 1)[0]
                setattr(get_data.GetData, 'cameraId', str(cameraId))
        with allure.step("处理相关数据依赖"):
            if test_result.cookies:  # 判断请求cookies是否为空
                cookies = requests.utils.dict_from_cookiejar(test_result.cookies)
                setattr(get_data.GetData, "COOKIES", cookies)
            if title == "登录接口正常验证":  # 提取token
                if test_result.json().get(extra):
                    token = test_result.json().get(extra)
                    setattr(get_data.GetData, "token", token)
        new_expected = json.loads(expected)  # 处理Null无法识别的问题
        # 输出测试结果和实际结果，进行断言比对，注意这里需要将实际结果的数据和预期结果的数据都改成字典类型，方便比对
        logger.info("测试结果：{}".format(test_result.json()))
        logger.info("预期结果：{}".format(new_expected))
        with allure.step("预期结果与实际响应进行断言操作"):
            try:
                self.analysis_check(new_expected, check_point_dict, test_result.json())
                result = "pass"
                logger.info("测试通过")
            except AssertionError as e:
                logger.error("测试失败，断言错误")
                result = "failed"
                logger.error(
                    F"请检查请求参数------------------- param:{param}\n url: {url}\n method: {method}\n header: {self.do_request.session.headers}")
                raise e
            finally:
                row = case_id + 1
                # 这里需要注意写回测试数据的时候，需要把测试数据转换成字符串类型
                with allure.step("将响应结果的内容写入用例中的实际结果栏"):
                    DoExcel(project_path.test_case_path, sheet_name).write_data(row, test_result.text, result)


if __name__ == '__main__':
    pytest.main(["-s", "--alluredir", "./allure", '--clean-alluredir', 'test_camera.py'])
    os.system("allure generate ./allure -o ./allure/html -c")
