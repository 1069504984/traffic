from common import get_data

__author__ = '李开'
import requests
import json
from common.my_log import MyLogg

mylog = MyLogg()


class DoRequests:
    '''完成http的get和post请求，并返回结果'''

    def __init__(self):
        self.session = requests.Session()

    def add_headers(self, headers):
        """添加公共请求头"""
        self.session.headers.update(headers)
        return self.session.headers

    def request(self, headers=None, cookies=None, url=None, method=None, param=None, files=None):

        if method == "get":
            try:
                rsp = self.session.get(url, headers=headers, params=param, cookies=cookies)
                mylog.my_info("get请求成功")
            except Exception as e:
                mylog.my_error("get请求发生异常".format(e))
                raise e
        elif method == "delete":
            try:
                rsp = self.session.delete(url, headers=headers, cookies=cookies, data=param, verify=False)
                mylog.my_info("delete请求成功")

            except Exception as e:
                mylog.my_error("delete请求发生异常".format(e))
                raise e
        elif method == "post":
            try:
                rsp = self.session.post(url, headers=headers, cookies=cookies, data=param, files=files,
                                        verify=False)
                mylog.my_info("post请求成功")
            except Exception as e:
                mylog.my_error("post请求发生异常".format(e))
                raise e
        elif method == "put":
            try:
                rsp = self.session.put(url, headers=headers, cookies=cookies, data=param, verify=False)
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
            test_result = DoRequests().request(headers=header,
                                               cookies=getattr(get_data.GetData, "COOKIES"), url=url, method=method,
                                               param=new_param)
        elif isinstance(new_param, dict) and modular == "上传视频":
            test_result = DoRequests().request(headers=header,
                                               cookies=getattr(get_data.GetData,
                                                               "COOKIES"), url=url, method=method, param=new_param,
                                               files=files)
        else:
            test_result = DoRequests().request(headers=header,
                                               cookies=getattr(get_data.GetData,
                                                               "COOKIES"), url=url, method=method,
                                               param=new_param.encode("utf-8"))
        return test_result


class HandleRequest(object):
    """
    处理请求
    """

    # def __init__(self, url, headers):
    #     self.url = url
    #     self.headers = headers

    def __init__(self):
        # 会话请求  适用于会话认证的项目
        self.one_session = requests.Session()

    def add_headers(self, headers):
        """添加公共请求头"""
        self.one_session.headers.update(headers)

    def send(self, url, data=None, method='post', is_json=True, **kwargs):
        # 1.data = '{字典}'   json格式字符串
        # 2.data = "{字典}"   字典类型字符串
        if isinstance(data, str):
            try:
                data = json.loads(data)
            except Exception as e:
                print("调用日志来处理记录")
                data = eval(data)

        method = method.lower()
        if method == 'get':
            res = self.one_session.request(method, url, params=data, **kwargs)
        elif method in ("post", "put", "delet"):
            if is_json:  # 如果is_json为True,那么以json格式的形式传参
                # res = self.one_session.post(url,json=data,**kwargs)
                res = self.one_session.request(method, url, json=data, **kwargs)
            else:  # 如果is_json为False,那么以www-form的形式传参
                # res = self.one_session.post(url,data=data,**kwargs)
                res = self.one_session.request(method, url, data=data, **kwargs)
        else:
            res = None
            print("不支持【{}】请求方法".format(method))
        return res

    def close(self):
        self.one_session.close()


if __name__ == '__main__':
    pass
