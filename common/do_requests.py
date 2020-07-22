from common import get_data

__author__ = '李开'
import requests
import json
from common.my_log import MyLogg

mylog = MyLogg()


class DoRequests:
    '''完成http的get和post请求，并返回结果'''

    def __init__(self, url, method, param=None, files=None):
        self.url = url
        self.method = method
        self.param = param
        self.files = files
        self.session = requests.Session()

    def request(self, headers=None, cookies=None):

        if self.method == "get":
            try:
                rsp = self.session.get(self.url, params=self.param, cookies=cookies)
                mylog.my_info("get请求成功")
            except Exception as e:
                mylog.my_error("get请求发生异常".format(e))
                raise e
        elif self.method == "delete":
            try:
                rsp = self.session.delete(self.url, headers=headers, cookies=cookies, data=self.param, verify=False)
                mylog.my_info("delete请求成功")

            except Exception as e:
                mylog.my_error("delete请求发生异常".format(e))
                raise e
        elif self.method == "post":
            try:
                rsp = self.session.post(self.url, headers=headers, cookies=cookies, data=self.param, files=self.files,
                                        verify=False)
                mylog.my_info("post请求成功")
            except Exception as e:
                mylog.my_error("post请求发生异常".format(e))
                raise e
        elif self.method == "put":
            try:
                rsp = self.session.put(self.url, headers=headers, cookies=cookies, data=self.param, verify=False)
                mylog.my_info("put请求成功")
            except Exception as e:
                mylog.my_error("put请求发生异常".format(e))
                raise e
        else:
            mylog.my_error("请求方式异常")
            rsp = None
        return rsp

    @staticmethod
    def be_result(item, param, url, method, header, files=None, modular=None):
        if "application/json" in item["header"]:
            new_param = param
        else:
            new_param = eval(param)
        if isinstance(new_param, tuple):
            test_result = DoRequests(url, method, new_param).request(headers=header,
                                                                     cookies=getattr(get_data.GetData, "COOKIES"))
        elif isinstance(new_param, dict) and modular == "上传视频":
            test_result = DoRequests(url, method, new_param, files=files).request(headers=header,
                                                                                  cookies=getattr(get_data.GetData,
                                                                                                  "COOKIES"))
        else:
            test_result = DoRequests(url, method, new_param.encode("utf-8")).request(headers=header,
                                                                                     cookies=getattr(get_data.GetData,
                                                                                                     "COOKIES"))
        return test_result


if __name__ == '__main__':
    pass
