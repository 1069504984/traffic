# -*- coding: utf-8 -*-
# @Time    : 2020/1/21 16:45
# @Author  : Fighter
from common.do_mysql import DoMysql
from common import get_data
from common.do_requests import DoRequests
from common.learn_do_excel import DoExcel
from common import project_path
from common.my_log import MyLogg
import requests
import json
import warnings
import allure
import pytest
import os

my_log = MyLogg()
test_data = DoExcel(project_path.test_case_path, "camera").read_data()


@allure.feature("监控点")
class TestCases():
    def setUp(self):  # 测试之前的准备工作
        warnings.simplefilter("ignore", ResourceWarning)

    def tearDown(self):
        pass

    @pytest.mark.parametrize('item', test_data)
    def test_001(self, item):
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
        header = eval(item["header"])
        sql = item["sql"]
        print(sql)
        param = get_data.GetData().replace(param)
        print("最终param-----{}".format(param))
        if sql is not None:
            sql = get_data.GetData().replace(sql)
            print("最终sql------{}".format(sql))
        my_log.my_info("正在发起{}模块中的第{}条用例:{}".format(modular, case_id, title))
        my_log.my_info("测试数据是：{}".format(param))
        test_result = DoRequests.be_result(item, param, url, method, header)  # 发起请求
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
        new_expected = json.loads(expected)  # 处理Null无法识别的问题
        # 输出测试结果和实际结果，进行断言比对，注意这里需要将实际结果的数据和预期结果的数据都改成字典类型，方便比对
        my_log.my_info("测试结果：{}".format(test_result.json()))
        my_log.my_info("预期结果：{}".format(new_expected))
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
            DoExcel(project_path.test_case_path, "camera").write_data(row, test_result.text, result)


if __name__ == '__main__':
    pytest.main(["-s", "--alluredir", "./allure", '--clean-alluredir', 'test_camera.py'])
    os.system("allure generate ./allure -o ./allure/html -c")
