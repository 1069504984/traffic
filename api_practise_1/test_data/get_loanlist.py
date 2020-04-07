__author__ = '程程'
#1引入单元测试，代替run这个文件
#2引入ddt，参数化我们测试用例里面的每一条数据，提高复用性，做法就是先获取excel文件中用例
#1）然后通过data传入（需要解包），然后将data里面的元祖的每一个元素，传入到函数中，再对传入的元素进行处理
#3测试用例里面引入try..except..finally，最后写回测试数据
#4测试报告--在run文件中进行运行
#5测试报告的路径



import unittest
from  common.do_mysql import DoMysql
from  common import get_data
from  common.do_requests import DoRequests
from  common.learn_do_excel import DoExcel
from  common import project_path
from ddt import ddt,data,unpack
from  common.my_log import MyLogg
my_log=MyLogg()
test_data=DoExcel(project_path.case_path,"getLoanList").read_data()
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
        url=item["url"]
        method=item["method"]
        param=item["param"]
        case_id=item["case_id"]
        modular=item["modular"]
        title=item["title"]
        expected=item["expected"]
        sql=item["sql"]
        param=get_data.GetData().replace(param)
        print("目前的param是{}".format(param))
        my_log.my_info("正在发起{}模块中的第{}条用例:{}".format(modular,case_id,title))
        my_log.my_info("测试数据是：{}".format(param))
        test_result=DoRequests(url,method,param=eval(param)).request(cookies=getattr(get_data.GetData,"COOKIES"))
        #增加一个判断
        if test_result.cookies:#判断请求cookies是否为空
            setattr(get_data.GetData,"COOKIES",test_result.cookies)
        my_log.my_info("测试结果是：{}".format(test_result.json()))
        my_log.my_info("预期结果是：{}".format(eval(expected)))
        try:
            self.assertEqual(eval(expected)["status"],test_result.json()["status"])
            self.assertEqual(eval(expected)["code"],test_result.json()["code"])
            result="pass"
            my_log.my_info("测试通过了")
        except AssertionError as e:
            my_log.my_error("测试失败，http请求发生错误")
            result="failed"
            raise e
        finally:
            row=case_id+1
            DoExcel(project_path.case_path,"getLoanList").write_data(row,test_result.text,result)#写回的数据格式必须是字符串或者数字类型才可以










