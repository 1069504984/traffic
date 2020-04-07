__author__ = '程程'
import unittest
from common.do_mysql import DoMysql
from  common import get_data
from  common.do_requests import DoRequests
from  common.learn_do_excel import DoExcel
from  common import project_path
from ddt import ddt,data,unpack
from  common.my_log import MyLogg
my_log=MyLogg()
test_data=DoExcel(project_path.case_path,"generate_repayments").read_data()
# print(test_data)
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
        #获取测试用例数据，数据类型基本都为字符串类型
        url=item["url"]
        method=item["method"]
        param=item["param"]
        case_id=item["case_id"]
        modular=item["modular"]
        title=item["title"]
        expected=item["expected"]
        sql=item["sql"]

         #参数化param
        param=get_data.GetData().replace(param)
        my_log.my_info("参数化之后param是{}".format(param))

        #参数化sql
        my_log.my_info("参数化之前的sql：".format(sql))
        if sql is not None:
         sql=get_data.GetData().replace(sql)
         my_log.my_info("参数化之后的sql是{}".format(sql))

        my_log.my_info("正在发起{}模块中的第{}条用例:{}".format(modular,case_id,title))

        #输入参数进行接口测试
        test_result=DoRequests(url,method,eval(param)).request(cookies=getattr(get_data.GetData,"COOKIES"))

        #获取用户的member_id
        if sql is not None and eval(sql)["sql_1"] is not None:
            member_id=DoMysql().do_mysql(eval(sql)["sql_1"],1)[0]
            setattr(get_data.GetData,"normal_member_id",str(member_id))

        #获取loan_id
        if sql is not None  and eval(sql)["sql_2"] is not None:
            sql=get_data.GetData().replace(sql)
            loan_id=DoMysql().do_mysql(eval(sql)["sql_2"],1)[0]
            setattr(get_data.GetData,"loan_id",str(loan_id))

        #投资之后，再做一个查询，查询数据库里面用户的余额
        #增加一个判断
        if test_result.cookies:#判断请求cookies是否为空
            setattr(get_data.GetData,"COOKIES",test_result.cookies)

        my_log.my_info("接口返回的http状态码：{}".format(test_result))
        my_log.my_info("测试结果是：{}".format(test_result.json()))
        my_log.my_info("预期结果是：{}".format(eval(expected)))

        try:
            self.assertEqual(eval(expected),test_result.json())
            result="pass"
            my_log.my_info("测试通过了")
        except AssertionError as e:
            my_log.my_error("测试失败，http请求发生错误")
            result="failed"
            raise e
        finally:
            row=case_id+1
            DoExcel(project_path.case_path,"generate_repayments").write_data(row,test_result.text,result)


