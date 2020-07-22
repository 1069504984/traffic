__author__ = 'Administrator'
import json
import requests
from common import project_path


class Do_Requests:
    def __init__(self):
        self.session = requests.Session()

    def __call__(self, url, method, data, *args, **kwargs):
        method = method.lower()
        if isinstance(data, str):
            try:
                data = json.loads(data)
            except Exception as e:
                print("".format(e))
                data = eval(data)

        if method == "get":
            res = self.session.get(url=url, params=data)
        elif method == "post":
            res = self.session.post(url=url, data=data)
        else:
            print("")
            res = None
        print(res.text)
        return res

    def close(self):
        self.session.close()


from openpyxl import load_workbook

import requests


class HttpRequest:
    '''该类完成http的get 以及post请求，并返回结果'''

    def http_request(self, method, url, param, cookies):  # 对象方法
        '''根据请求方法来决定发起get请求还是post请求
        method: get post http的请求方式
        url:发送请求的接口地址
        param:随接口发送的请求参数 以字典格式传递
        rtype:有返回值，返回结果是响应报文
        '''
        global COOKIES
        global resp
        if method.upper() == 'GET':
            try:
                resp = requests.get(url, params=param, cookies=cookies)  # 传递cookies
            except Exception as e:
                print('get请求出错了：{}'.format(e))
        elif method.upper() == 'POST':
            try:
                resp = requests.post(url, data=param, cookies=cookies)  # 传递cookies
            except Exception as e:
                print('post请求出错了：{}'.format(e))
        else:
            print('不支持该种方式')
            resp = None
        return resp


if __name__ == '__main__':
    HttpRequest().http_request()

# if __name__ == '__main__':
#     url = "http://test.lemonban.com/futureloan/mvc/api/member/login"
#     method = "GET"
#     param = '{"mobilephone":"15815541763","pwd":"tudou123456"}'
#
#     # print(data.json())
#     url_1 = "http://test.lemonban.com/futureloan/mvc/api/member/withdraw"
#     method = "get"
#     param_1 = {"mobilephone": "15815541763", "amount": "100"}
#
#     headers = {
#         "User-Agent": "Mozilla/5.0"
#     }
#     # send_request = HttpRequest()
#     # # 登录
#     # send_request(method='POST', url=url, data=param, is_json=False, headers=headers)
#     # # 充值
#     # send_request(method='PoST', url=url_1, data=param_1)
#
#     do_session = Do_Requests()
#     # 登录
#     do_session(url=url, method=method, data=param)
#     # 提现
#     do_session(url=url_1, method=method, data=param_1)
