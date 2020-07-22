from common.do_mysql import DoMysql
from common import get_data
from common.do_requests import DoRequests
from common.learn_do_excel import DoExcel
from common import project_path
from common.my_log import MyLogg
import requests
import json
import warnings
import pytest
import allure
import os

my_log = MyLogg()
test_data = DoExcel(project_path.test_case_path, "query_task").read_data()


@allure.feature("各种查询任务接口")
class TestCases():
    def setUp(self):  # 测试之前的准备工作
        warnings.simplefilter("ignore", ResourceWarning)

    def tearDown(self):
        pass

    @pytest.mark.parametrize('item', test_data)
    def test_001(self, item):
        '''
        监控点接口
        '''
        global result  # 指明全局变量
        global files
        global COOKIES  # 设置cookies为全局变量
        allure.dynamic.title(item['title'])
        allure.dynamic.description(item['title'])
        # 获取item中的用例数据
        url = item["url"]
        url = get_data.GetData().replace(url)
        method = item["method"]
        modular = item["modular"]
        param = item["param"]  # 返回的是字符串类型的数据
        if modular == "上传视频":
            files = eval(item["param"])[-1]
            param = str(eval(item["param"])[0])
        case_id = item["case_id"]
        title = item["title"]
        expected = item["expected"]
        header = eval(item["header"])
        sql = item["sql"]
        print(sql)
        param = get_data.GetData().replace(param)
        print("目前的param是{}".format(param))
        if sql is not None:
            sql = get_data.GetData().replace(sql)
            print("现在的sql是{}".format(sql))
        my_log.my_info("正在发起{}模块中的第{}条用例:{}".format(modular, case_id, title))
        my_log.my_info("测试数据是：{}".format(param))
        # 执行接口测试，cookies利用反射进行动态的获取

        test_result = DoRequests.be_result(item, param, url, method, header)
        # if "data" in test_result.json() and test_result.json()["data"] is not None and len(test_result.json()["data"]["fileId"]) <= 18:
        #     setattr(get_data.GetData, "fileId", test_result.json()["data"]["fileId"])
        print(test_result.text)
        if getattr(get_data.GetData, 'cameraId') != "None":
            print("删除的camemaId:{}".format(getattr(get_data.GetData, 'cameraId')))
        if test_result.cookies:  # 判断请求cookies是否为空
            cookies = requests.utils.dict_from_cookiejar(test_result.cookies)
            setattr(get_data.GetData, "COOKIES", cookies)
        new_expected = json.loads(expected)  # 处理Null无法识别的问题
        # 输出测试结果和实际结果，进行断言比对，注意这里需要将实际结果的数据和预期结果的数据都改成字典类型，方便比对
        my_log.my_info("测试结果是：{}".format(test_result.json()))
        my_log.my_info("预期结果是：{}".format(new_expected))
        try:
            assert new_expected["code"] == test_result.json()["code"]
            result = "pass"
            my_log.my_info("测试通过了")
        except AssertionError as e:
            my_log.my_error("测试失败，断言错误")
            result = "failed"
            raise e
        finally:
            row = case_id + 1
            # 这里需要注意写回测试数据的时候，需要把测试数据转换成字符串类型
            DoExcel(project_path.test_case_path, "query_task").write_data(row, test_result.text, result)


if __name__ == '__main__':
    pytest.main(["-s", "--alluredir", "./allure", '--clean-alluredir', 'test_query_task.py'])
    os.system("allure generate ./allure -o ./allure/html -c")
