from common.do_requests import DoRequests
from common.learn_do_excel import DoExcel
from common import project_path
from ddt import ddt, data, unpack
from common.log_demo import logger
import json
import allure
import pytest


test_data = DoExcel(project_path.test_case_path, "login").read_data()


@allure.feature("监控点")
class TestCases():
    def setUp(self):  # 测试之前的准备工作
        pass

    def tearDown(self):
        pass

    @pytest.mark.parametrize('item', test_data)
    def test_001(self, item):
        '''
        登录用例
        '''
        global result  # 指明全球变量
        url = item["url"]
        method = item["method"]
        param = item["param"]
        case_id = item["case_id"]
        modular = item["modular"]
        title = item["title"]
        header = eval(item["header"])
        expected = item["expected"]
        logger.info("正在发起{}模块中的第{}条用例:{}".format(modular, case_id, title))
        logger.info("测试数据是：{}".format(param))
        new_param = json.dumps(eval(param))
        test_result = DoRequests(url, method, new_param).request(header)
        # logger.info("测试结果是：{}".format(test_result.json()))
        # logger.info("测试结果是：{}".format(test_result.text))
        new_expected = json.loads(expected)
        logger.info("预期结果是：{}".format(new_expected))
        new_result = test_result.json()
        new_result2 = new_result.pop("timestamp")
        logger.info("已删除当前需要断言的登录时间:timestamp: {}".format(new_result2))
        try:
            self.assertEqual(new_expected, new_result)
            logger.info("实际结果是：{}".format(new_result))
            logger.info("测试通过了")
            result = "pass"
        except AssertionError as e:
            logger.error("测试不通过，断言结果有误")
            result = "failed"
            raise e
        finally:
            row = case_id + 1
            DoExcel(project_path.case_path, "login").write_data(row, test_result.text, result)  # 写回的数据格式必须是字符串或者数字类型才可以
