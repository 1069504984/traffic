__author__ = '程程'
import requests
import json
from common.my_log import MyLogg

mylog = MyLogg()


class DoRequests:
    '''完成http的get和post请求，并返回结果'''

    def __init__(self, url, method, param=None):
        self.url = url
        self.method = method
        self.param = param

    def get_header(self,index):
        if index == 1:
            headers = {
                'Connection': 'keep-alive',
                'Accept': 'application/json, text/javascript, */*; q=0.01',
                'Origin': 'http://172.16.1.107:9088',
                'X-Requested-With': 'XMLHttpRequest',
                'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJrZW4iLCJpYXQiOjE1Mzc1NTQzMDksImRhdGEiOnsidXNlcm5hbWUiOiJ4dXRvbmdiYW8iLCJpc19zdXBlcnVzZXIiOjEsImlkIjoxNywibG9naW5fdGltZSI6MTUzNzU1NDMwOX0sImV4cCI6MTUzODE1NDMwOX0.32Lys4hjjY2XRpM2r9YSmpYA798u821m_M5Tzb6wxIU',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36',
                'Content-Type': 'application/json',
                'Accept-Encoding': 'gzip, deflate',
                'Accept-Language': 'zh-CN,zh;q=0.9',
            }
        elif index == 2:
            headers = {
                'Connection': 'keep-alive',
                'Accept': 'application/json, text/javascript, */*; q=0.01',
                'Origin': 'http://172.16.1.107:9088',
                'X-Requested-With': 'XMLHttpRequest',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36',
                'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                'Referer': 'http://172.16.1.107:9088/warningDealWith',
                'Accept-Encoding': 'gzip, deflate',
                'Accept-Language': 'zh-CN,zh;q=0.9',
            }

        return headers





    def request(self,headers=None, cookies=None):
        if self.method == "get":
            try:
                rsp = requests.get(self.url, params=self.param, cookies=cookies)
                mylog.my_info("get请求成功")
            except Exception as e:
                mylog.my_error("get请求发生异常".format(e))
                raise e
        elif self.method == "post":
            try:
                rsp = requests.post(self.url,headers=headers,cookies=cookies,data=self.param, verify=False)
                mylog.my_info("post请求成功")
            except Exception as e:
                mylog.my_error("post请求发生异常".format(e))
                raise e
        else:
            mylog.my_error("请求方式异常")
            rsp = None
        return rsp


class HanleRequests:
    def __init__(self, url, method, param):
        self.url = url
        self.method = method
        self.param = param

    def request_1(self):
        if self.method == "get":
            data = requests.get(self.url, self.param)
        elif self.method == "post":
            data = requests.post(self.url, self.param)
        else:
            print("failed")
        return data


if __name__ == '__main__':
    url1 = "https://www.ketangpai.com/"
    method1 = "post"
    # param1={"username":"admin","password":"1cd73874884db6a0f9f21d853d7e9eacdc773c39ee389060f5e96ae0bcb4773a"}
    param2 = {"email": 13677330113, "password": "kaililikai", "remember": 0}
    data = DoRequests(url1, method1, param2).request()
    print(data.headers)

    url2 = "https://www.ketangpai.com/VipApi/isVip"
    method2 = "get"
    param3 = {"groupId": "GID_INTERACT", "httptype": 1}
    header = None

    data2 = DoRequests(url2, method2, param3).request()
    print(json.dumps(data2.json()))
    print(type(json.dumps(data2.json())))
    #
    url3 = "https://www.ketangpai.com/HomeworkApi/listsHomework?courseid=MDAwMDAwMDAwMLOsvZmIuatp"
    method3 = "get"
    param4 = {"courseid": "MDAwMDAwMDAwMLOsvZmIuatp"}

    data3 = DoRequests(url3, method3, param4).request(cookies=data2.cookies)
    print(data.json())

    # print(data.headers["Set-Cookie"].split(";")[0])
    # url="http://172.16.1.76:9088/resultQuery/getWarningDetail"
    # method = "post"
    # param = {'flag':'2202001080501346065727447615554970064089509095271,122'}
    # data=DoRequests(url,method,param).request(data.cookies)
    # print(data.text)
