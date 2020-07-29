# -*- coding: utf-8 -*-
# @Time    : 2020/5/18 14:55
# @Author  : Fighter
import pytest
import requests
import pytest

data = [1, 2]


class TestCases():
    @pytest.mark.parametrize('a', data)
    @pytest.mark.usefixtures("add_camera_task")
    def test_parametrize(self, a):
        print('\n被加载测试数据为\n{}'.format(a))


if __name__ == '__main__':
    # pytest.main(['-s', 'test_demo.py::TestCases'])
    header = {'User-Agent': 'python-requests/2.22.0', 'Accept-Encoding': 'gzip, deflate', 'Accept': '*/*',
              'Connection': 'keep-alive', 'authorization': 'Basic ZWxhc3RpYzoxMjM0NTY=',
              'keensense-traffic-token': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE1OTYwODA0MDc0NjksInBheWxvYWQiOiIxIn0.0usgBYzZbMofTbx0-JEiuzvB1b4q5aMRF-QP-YN6hcQ',
              'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'}

    params = (
        ('cameraId', '1562225808264'),
    )

    response = requests.get('http://172.16.1.107:9088/api_traffic/camera/isAnalyzed', headers=header, params=params)
    print(response.text)
