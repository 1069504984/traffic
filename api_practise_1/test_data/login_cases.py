__author__ = '程程'
#1引入单元测试，代替run这个文件
#2引入ddt，参数化我们测试用例里面的每一条数据，提高复用性，做法就是先获取excel文件中用例
#1）然后通过data传入（需要解包），然后将data里面的元祖的每一个元素，传入到函数中，再对传入的元素进行处理
#3测试用例里面引入try..except..finally，最后写回测试数据
#4测试报告--在run文件中进行运行
#5测试报告的路径




import unittest
from  common.do_requests import DoRequests
from  common.learn_do_excel import DoExcel
from  common import project_path
from ddt import ddt,data,unpack
from  common.my_log import MyLogg
import json
my_log=MyLogg()
test_data=DoExcel(project_path.case_path,"login").read_data()
@ddt
class TestCases(unittest.TestCase):
    def setUp(self):#测试之前的准备工作
        pass
    def tearDown(self):
       pass
    @data(*test_data)
    def test_001(self,item):
        global result#指明全球变量
        url=item["url"]
        method=item["method"]
        param=item["param"]
        case_id=item["case_id"]
        modular=item["modular"]
        title=item["title"]
        expected=item["expected"]
        my_log.my_info("正在发起{}模块中的第{}条用例:{}".format(modular,case_id,title))
        my_log.my_info("测试数据是：{}".format(param))
        new_param = json.dumps(eval(param))
        headers = DoRequests(url, method, new_param).get_header(index=1)
        test_result=DoRequests(url,method,new_param).request(headers)
        # my_log.my_info("测试结果是：{}".format(test_result.json()))
        # my_log.my_info("测试结果是：{}".format(test_result.text))
        new_expected=json.loads(expected)
        my_log.my_info("预期结果是：{}".format(new_expected))
        new_result=test_result.json()
        new_result2=new_result.pop("timestamp")
        my_log.my_info("已删除当前需要断言的登录时间:timestamp: {}".format(new_result2))
        try:
            self.assertEqual(new_expected,new_result)
            my_log.my_info("实际结果是：{}".format(new_result))
            my_log.my_info("测试通过了")
            result="pass"
        except AssertionError as e:
            my_log.my_error("http请求发生错误")
            result="failed"
            raise e
        finally:
            row=case_id+1
            DoExcel(project_path.case_path,"login").write_data(row,test_result.text,result)#写回的数据格式必须是字符串或者数字类型才可以










