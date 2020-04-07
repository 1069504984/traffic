__author__ = '程程'
import unittest
from common.do_mysql import DoMysql
from common import get_data
from common.do_requests import DoRequests
from common.learn_do_excel import DoExcel
from common import project_path
from ddt import ddt, data
from common.my_log import MyLogg

my_log = MyLogg()
test_data = DoExcel(project_path.case_path, "invest").read_data()
print(test_data)

@ddt
class TestCases(unittest.TestCase):
    def setUp(self):  # 测试之前的准备工作
        pass

    def tearDown(self):
        pass

    @data(*test_data)
    def test_001(self,item):
        global result  # 指明全局变量
        global COOKIES  # 设置cookies为全局变量
        global before_amount
        url = item["url"]
        method = item["method"]
        param = item["param"]
        case_id = item["case_id"]
        modular = item["modular"]
        title = item["title"]
        expected = item["expected"]
        sql = item["sql"]
        param = get_data.GetData().replace(param)
        print("目前的param是{}".format(param))
        if sql is not None:
            sql = get_data.GetData().replace(sql)
            print("目前的sql是{}".format(sql))
            before_amount = DoMysql().do_mysql(eval(sql)["sql"])[0]
            my_log.my_info("充值之前账户余额：{}".format(before_amount))
        my_log.my_info("正在发起{}模块中的第{}条用例:{}".format(modular, case_id, title))
        my_log.my_info("测试数据是：{}".format(param))
        test_result = DoRequests(url, method, eval(param)).request(cookies=getattr(get_data.GetData, "COOKIES"))
        # 增加一个判断
        if test_result.cookies:  # 判断请求cookies是否为空
            setattr(get_data.GetData, "COOKIES", test_result.cookies)
        my_log.my_info("测试结果是：{}".format(test_result.text))
        my_log.my_info("预期结果是：{}".format(eval(expected)))
        try:
            self.assertEqual(eval(expected)["code"],test_result.json()["total"])
        #     if sql is not None:
        #         after_amount = DoMysql().do_mysql(eval(sql)["sql"], 1)[0]
        #         recharge_amount = int(eval(param)["amount"])
        #         my_log.my_info("充值的金额是：{}".format(str(recharge_amount)))
        #         expected_amount = recharge_amount + before_amount
        #         my_log.my_info("充值之后的用户余额：{}".format(expected_amount))
        #         self.assertEqual(expected_amount, after_amount)
        #         expected = expected.replace("expectedamount", str(expected_amount))
        #     self.assertEqual(eval(expected)["status"], test_result.json()["status"])
        #     self.assertEqual(eval(expected)["code"], test_result.json()["code"])
        #     self.assertEqual(eval(expected)["msg"], test_result.json()["msg"])
            result = "pass"
            my_log.my_info("测试通过了")
        except AssertionError as e:
            my_log.my_error("测试失败，http请求发生错误")
            result = "failed"
            raise e
        finally:
            row = case_id + 1
            DoExcel(project_path.case_path, "invest").write_data(row, test_result.text, result)
