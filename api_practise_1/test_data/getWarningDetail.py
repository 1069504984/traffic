__author__ = '程程'
import unittest
from  common.do_mysql import DoMysql
from  common import get_data
from  common.do_requests import DoRequests
from  common.learn_do_excel import DoExcel
from  common import project_path
from ddt import ddt,data,unpack
from  common.my_log import MyLogg
import json
import requests
my_log=MyLogg()
test_data=DoExcel(project_path.case_path,"getWarningDetail").read_data()
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
        url=item["url"]
        method=item["method"]
        param=item["param"]
        case_id=item["case_id"]
        modular=item["modular"]
        title=item["title"]
        expected=item["expected"]
        sql=item["sql"]
        # print(sql)
        param=get_data.GetData().replace(param)
        print("现在的param是{}".format(param))
        # if sql is not None:
        #  sql=get_data.GetData().replace(sql)
        #  print("现在的sql是{}".format(sql))
        #
        # if sql is not None  and eval(sql)["sql_2"] is not None:
        #     sql_result=DoMysql().do_mysql(eval(sql)["sql_2"],2)
        #     my_log.my_info("交易记录是：{}".format(sql_result))

        my_log.my_info("正在发起{}模块中的第{}条用例:{}".format(modular,case_id,title))
        my_log.my_info("测试数据是：{}".format(param))

        if case_id == 1:
            new_param = json.dumps(eval(param))
            headers = DoRequests(url, method, new_param).get_header(index=1)
        else:
            new_param = json.loads(param)
            headers = DoRequests(url, method, new_param).get_header(index=2)
        test_result=DoRequests(url,method,new_param).request(headers=headers,cookies=getattr(get_data.GetData,"COOKIES"))
        print(test_result.text)

        #获取loan_id
        # if sql is not None  and eval(sql)["sql_1"] is not None:
        #     sql=get_data.GetData().replace(sql)
        #     member_id=DoMysql().do_mysql(eval(sql)["sql_1"],1)[0]
        #     setattr(get_data.GetData,"normal_member_id",str(member_id))
        # if sql is not None  and eval(sql)["sql_2"] is not None:
        #     sql=get_data.GetData().replace(sql)
        #     sql_result=DoMysql().do_mysql(eval(sql)["sql_2"],1)[0]
        #增加一个判断
        if test_result.cookies:#判断请求cookies是否为空  # c = requests.cookies.RequestsCookieJar()# c.set('cookie-name', 'cookie-value', path='/', domain='.abc.com')# s.cookies.update(c)
            cookies = requests.utils.dict_from_cookiejar(test_result.cookies)
            setattr(get_data.GetData,"COOKIES",cookies)
        new_expected=json.loads(expected)
        my_log.my_info("测试结果是：{}".format(test_result.json()))
        my_log.my_info("预期结果是：{}".format(new_expected))
        try:
            self.assertEqual(new_expected["code"],test_result.json()["code"])
            result="pass"
            my_log.my_info("测试通过了")
        except Exception as e:
            my_log.my_error("测试失败，http请求发生错误")
            result="failed"
            raise e
        finally:
            row=case_id+1
            DoExcel(project_path.case_path,"getWarningDetail").write_data(row,test_result.text,result)

