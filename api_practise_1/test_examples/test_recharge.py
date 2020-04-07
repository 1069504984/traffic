
from ddt import ddt,data

__author__ = 'Administrator'
import unittest
from  common.learn_do_excel import DoExcel
from  common.cs import Do_Requests
from  common.do_requests import DoRequests
from  common import project_path
from  common import get_data
from  common.my_log import MyLogg
mylog=MyLogg()
test_data=DoExcel(project_path.exampels_path,"recharge").read_data()
print(test_data)
@ddt
class TestCases(unittest.TestCase):
    @data(*test_data)
    def test_001(self,item):
        global param
        global url
        global method
        global case_id
        global modular
        global title
        global expected



        url=item["url"]
        method=item["method"]
        param=item["param"]
        case_id=item["case_id"]
        modular=item["modular"]
        title=item["title"]
        expected=item["expected"]
        sql=item["sql"]

        param=get_data.GetData().replace(param)
        mylog.my_info("参数化之后param是{}".format(param))


        headers = {"User-Agent": "Mozilla/5.0"}
        test_result=DoRequests(url,method,eval(param)).request(cookies=getattr(get_data.GetData,"COOKIES"))
        # do_session = Do_Requests()
        # # 登录
        # test_result=do_session(url=url, method=method, data=param,headers=headers)




        if test_result.cookies:#判断请求cookies是否为空
                setattr(get_data.GetData,"COOKIES",test_result.cookies)

        mylog.my_info("接口返回的http状态码：{}".format(test_result))
        if case_id == 2:
            mylog.my_info("测试结果是：{}".format(test_result))
            mylog.my_info("预期结果是：{}".format(expected))
        else:
            mylog.my_info("测试结果是：{}".format(test_result.json()))
            mylog.my_info("预期结果是：{}".format(eval(expected)))


        try:
            self.assertEqual(eval(expected)["Code"],test_result.json()["Code"])
            self.assertEqual(eval(expected)["Message"],test_result.json()["Message"])
            result="pass"
            mylog.my_info("测试通过了")
        except AssertionError as e:
            mylog.my_error("测试失败，http请求发生错误")
            result="failed"
            raise e
        finally:
            row=case_id+1
            DoExcel(project_path.case_path,"generate_repayments").write_data(row,test_result.text,result)









