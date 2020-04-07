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
my_log = MyLogg()
test_data = DoExcel(project_path.case_path, "getserialnumber").read_data()


@ddt
class TestCases(unittest.TestCase):
    def setUp(self):  # 测试之前的准备工作
        pass

    def tearDown(self):
        pass

    @data(*test_data)
    def test_001(self, item):
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

        # 如果有sql则把sql中需要参数化的量去进行替换
        if sql is not None:
            sql = get_data.GetData().replace(sql)
            my_log.my_info("现在的sql是{}".format(sql))

        # param不管里面是否有参数化都可以替代，反正返回的还是param本身，找到一个返回一个
        param = get_data.GetData().replace(param)

        my_log.my_info("正在发起{}模块中的第{}条用例:{}".format(modular, case_id, title))
        my_log.my_info("测试数据是：{}".format(param))

        # 执行接口测试，cookies利用反射进行动态的获取
        if case_id == 1:
            new_param = json.dumps(eval(param))
            headers = DoRequests(url, method, new_param).get_header(index=1)
        else:
            if title == "查找文件名":
                new_param = eval(param)
            else:
                new_param = json.loads(param)
            headers = DoRequests(url, method, new_param).get_header(index=2)
        test_result = DoRequests(url, method, new_param).request(headers=headers,
                                                                 cookies=getattr(get_data.GetData, "COOKIES"))
        print(test_result.text)

        # 增加一个判断如果第一个sql不为空则执行sql并取出第一个值，反射给类属性
        # 将前一个接口的结果传递给下一个作为测试数据
        if sql is not None and eval(sql)["sql_1"] is not None:
            member_id = DoMysql().do_mysql(eval(sql)["sql_1"], 1)[0]
            setattr(get_data.GetData, "normal_member_id", str(member_id))
            my_log.my_info("目前到的member_id是：{}".format(member_id))

        if sql is not None and eval(sql)["sql_2"] is not None:  # 如果测试用例中的query不为none就进行数据库查询操作
            loan_id = DoMysql().do_mysql(eval(sql)["sql_2"], 1)[0]
            # 这里将loanid的数据反射回去的时候，需要对loanid的数据进行处理的原因是，后面需要用到替代函数，只有字符串才能替代
            setattr(get_data.GetData, "loan_id", str(loan_id))
            my_log.my_info("目前的loan_id是：{}".format(getattr(get_data.GetData, "loan_id")))

        # 增加一个判断 是在完成完请求之后才去判断
        if test_result.cookies:  # 判断请求cookies是否为空
            cookies = requests.utils.dict_from_cookiejar(test_result.cookies)
            setattr(get_data.GetData, "COOKIES", cookies)
        new_expected = json.loads(expected) # 处理Null无法识别的问题

        # 输出测试结果和实际结果，进行断言比对，注意这里需要将实际结果的数据和预期结果的数据都改成字典类型，方便比对
        my_log.my_info("测试结果是：{}".format(test_result.json()))
        my_log.my_info("预期结果是：{}".format(new_expected))
        try:
            self.assertEqual(new_expected["code"], test_result.json()["code"])
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
