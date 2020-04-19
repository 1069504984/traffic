__author__ = '程程'

import unittest
from common.do_mysql import DoMysql
from common import get_data
from common.do_requests import DoRequests
from common.learn_do_excel import DoExcel
from common import project_path
from ddt import ddt, data, unpack
from common.my_log import MyLogg
import requests
import json
import pytest
import os
my_log = MyLogg()
test_data = DoExcel(project_path.case_path, "getserialnumber").read_data()


# def login():
#     test_data = DoExcel(project_path.case_path, "camera").read_data()[0]
#     test_result = DoRequests(test_data["url"], test_data["method"], eval(test_data["param"])).request(headers=test_data["header"],
#                                                               cookies=getattr(get_data.GetData, "COOKIES"))
#     yield requests.utils.dict_from_cookiejar(test_result.cookies)
#     print("cookies返回成功")


class TestCases():
    @pytest.mark.parametrize('item', test_data)
    def test_001(self, item,login):
        global result  # 指明全球变量
        global COOKIES  # 设置cookies为全局变量

        # 获取item中的用例数据
        url = item["url"]
        method = item["method"]
        param = item["param"]  # 返回的是字符串类型的数据
        case_id = item["case_id"]
        modular = item["modular"]
        title = item["title"]
        expected = item["expected"]
        sql = item["sql"]
        header = eval(item["header"])

        # 如果有sql则把sql中需要参数化的量去进行替换
        if sql is not None:
            sql = get_data.GetData().replace(sql)
            my_log.my_info("现在的sql是{}".format(sql))

        # param不管里面是否有参数化都可以替代，反正返回的还是param本身，找到一个返回一个
        param = get_data.GetData().replace(param)

        my_log.my_info("正在发起{}模块中的第{}条用例:{}".format(modular, case_id, title))
        my_log.my_info("测试数据是：{}".format(param))

        # 执行接口测试，cookies利用反射进行动态的获取
        if "application/json" in header["Content-Type"]:
            new_param = param
        else:
            new_param = eval(param)
        test_result = DoRequests(url, method, new_param).request(headers=header,
                                                                 cookies=getattr(get_data.GetData, "COOKIES"))
        print(test_result.text)

        # 增加一个判断 是在完成完请求之后才去判断
        if test_result.cookies:
            cookies = requests.utils.dict_from_cookiejar(test_result.cookies)
            setattr(get_data.GetData, "COOKIES", cookies)
        new_expected = json.loads(expected) # 处理Null无法识别的问题

        my_log.my_info("测试结果是：{}".format(test_result.json()))
        my_log.my_info("预期结果是：{}".format(new_expected))
        try:
            assert new_expected["code"]== test_result.json()["code"]
            result = "pass"
            my_log.my_info("测试通过了")
        except AssertionError as e:
            my_log.my_error("测试失败，http请求发生错误")
            result = "failed"
            raise e
        finally:
            row = case_id + 1
            # 这里需要注意写回测试数据的时候，需要把测试数据转换成字符串类型
            DoExcel(project_path.case_path, "getserialnumber").write_data(row, test_result.text, result)

if __name__ == '__main__':
    pytest.main([ "-s","--alluredir","./allure",'--clean-alluredir','test_get.py'])
    os.system("allure generate ./allure -o ./allure/html -c")
