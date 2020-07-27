# -*- coding: utf-8 -*-
# @Time    : 2020/4/26 15:00
# @Author  : Fighter
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
import Json_file
import os

current_path = os.path.dirname(__file__)
json_path = os.path.split(current_path)[0] + r"/Json_file"
my_log = MyLogg()
test_data = DoExcel(project_path.test_case_path, "structuring").read_data()[0:2]


# test_data3=DoExcel(project_path.case_path,"video").read_data()[0:3]

@allure.feature("结构化查询")
class TestCases():
    def setUp(self):  # 测试之前的准备工作
        warnings.simplefilter("ignore", ResourceWarning)

    def tearDown(self):
        pass

    @pytest.mark.parametrize('item', test_data)
    def test_list(self, item, test_login):
        print("完成前置")
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
        print("目前的param是{}".format(param))
        if sql is not None:
            sql = get_data.GetData().replace(sql)
            print("现在的sql是{}".format(sql))
        my_log.my_info("正在发起{}模块中的第{}条用例:{}".format(modular, case_id, title))
        my_log.my_info("测试数据是：{}".format(param))
        test_result = DoRequests.be_result(item, param, url, method, header)
        print(len(test_result.json()['data']))
        new_expected = json.loads(expected)  # 处理Null无法识别的问题
        my_log.my_info("测试结果是：{}".format(test_result.json()))
        my_log.my_info("预期结果是：{}".format(new_expected))
        try:
            assert new_expected["code"] == test_result.json()["code"]
            assert len(test_result.json()['data']) >= 0
            result = "pass"
            my_log.my_info("测试通过了")
        except AssertionError as e:
            my_log.my_error("测试失败，断言错误")
            result = "failed"
            raise e
        finally:
            row = case_id + 1
            # 这里需要注意写回测试数据的时候，需要把测试数据转换成字符串类型
            DoExcel(project_path.test_case_path, "structuring").write_data(row, str(test_result.json()["codeMsg"]),
                                                                           result)

    @allure.feature("excel导出")
    def test_export_excel(self):
        allure.dynamic.title("excel导出功能")
        with open(json_path + r'/export_excel.json', "r") as f:
            data = f.read()
            headers = {'Content-Type': 'application/json'}
            response = requests.post('http://172.16.1.107:9088/objext/download', headers=headers,
                                     cookies=getattr(get_data.GetData, "COOKIES"),
                                     data=data, verify=False)
            assert 200 == response.status_code
            result = "pass"
            DoExcel(project_path.test_case_path, "structuring").write_data(4, str(response.status_code), result)


if __name__ == '__main__':
    pytest.main(["-s", "--alluredir", "./allure", '--clean-alluredir', 'test_structuring.py'])
    # os.system("allure generate ./allure -o ./allure/html -c")
