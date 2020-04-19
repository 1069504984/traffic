# -*- coding: utf-8 -*-
# @Time    : 2020/4/19 15:47
# @Author  : lk

from common import get_data
from common.do_requests import DoRequests
from common.learn_do_excel import DoExcel
from common import project_path
from common.my_log import MyLogg
import requests
import pytest
my_log = MyLogg()
test_data = DoExcel(project_path.case_path, "getserialnumber").read_data()
@pytest.fixture()
def login():
    test_data = DoExcel(project_path.case_path, "camera").read_data()[0]
    test_result = DoRequests(test_data["url"], test_data["method"], test_data["param"]).request(headers=eval(test_data["header"]),
                                                              cookies=getattr(get_data.GetData, "COOKIES"))
    if test_result.cookies:
        cookies=requests.utils.dict_from_cookiejar(test_result.cookies)
        setattr(get_data.GetData, "COOKIES", cookies)
    print("cookies返回成功")