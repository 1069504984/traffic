__author__ = '程程'
import unittest
from  common.do_mysql import DoMysql
from  common import get_data
from  common.do_requests import DoRequests
from  common.learn_do_excel import DoExcel
from  common import project_path
from ddt import ddt,data,unpack
from  common.my_log import MyLogg
my_log=MyLogg()
test_data=DoExcel(project_path.case_path,"withdraw").read_data()
@ddt
class TestCases(unittest.TestCase):
    def setUp(self):#测试之前的准备工作
        pass
    def tearDown(self):
        pass
    @data(*test_data)
    def test_001(self,item):
        global result#指明全球变量
        global COOKIES#设置cookies为全局变量
        global before_amount
        global withdraw_amount
        url=item["url"]
        method=item["method"]
        param=item["param"]
        case_id=item["case_id"]
        modular=item["modular"]
        title=item["title"]
        expected=item["expected"]
        sql=item["sql"]

        #参数化测试数据
        param=get_data.GetData().replace(param)
        my_log.my_info("目前的param是{}".format(param))

        #判断是否需要执行sql 如果需要执行则运行代码
        if sql is not None:
            sql=get_data.GetData().replace(sql)
            print("目前的sql是{}".format(sql))
            before_amount=DoMysql().do_mysql(eval(sql)["sql"])[0]
            my_log.my_info("体现之前的用户余额是：{}".format(before_amount))

        my_log.my_info("正在发起{}模块中的第{}条用例:{}".format(modular,case_id,title))

        #传入参数 进行接口测试
        test_result=DoRequests(url,method,eval(param)).request(cookies=getattr(get_data.GetData,"COOKIES"))
        # print(test_result)

        #打印测试结果与实际结果
        # my_log.my_info("目前的测试结果是{}".format(test_result.json()))
        # my_log.my_info("预期结果是：{}".format(eval(expected)))

        #增加一个判断 传递cookies
        if test_result.cookies:#判断请求cookies是否为空
            setattr(get_data.GetData,"COOKIES",test_result.cookies)

        #打印出测试结果与预期结果
        my_log.my_info("测试结果是：{}".format(test_result.json()))
        my_log.my_info("预期结果是：{}".format(eval(expected)))

        #测试结果与预期结果进行断言
        try:
            if sql is not None:
                after_amount=DoMysql().do_mysql(eval(sql)["sql"],1)[0]
                my_log.my_info("提现之后的用户余额是：{}".format(after_amount))
                withdraw_amount=int(eval(param)["amount"])
                my_log.my_info("提现金额是：{}".format(str(withdraw_amount)))
                expected_amount=before_amount-withdraw_amount
                self.assertEqual(expected_amount,after_amount)
                expected=expected.replace("expectedamount",str(expected_amount))
                my_log.my_info("预期的用户余额是：{}".format(expected_amount))
            self.assertEqual(eval(expected)["status"],test_result.json()["status"])
            self.assertEqual(eval(expected)["code"],test_result.json()["code"])
            self.assertEqual(eval(expected)["msg"],test_result.json()["msg"])
            result="pass"
            my_log.my_info("测试通过了")
        except AssertionError as e:
            my_log.my_error("测试失败，http请求发生错误")
            result="failed"
            raise e
        finally:
            #写回测试结果
            row=case_id+1
            DoExcel(project_path.case_path,"withdraw").write_data(row,test_result.text,result)

