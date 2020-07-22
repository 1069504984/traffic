# -*- coding: utf-8 -*-
# @Time    : 2020/5/18 14:55
# @Author  : Fighter
import pytest

import pytest

data = [1, 2]


class TestCases():
    @pytest.mark.parametrize('a', data)
    @pytest.mark.usefixtures("add_camera_task")
    def test_parametrize(self, a):
        print('\n被加载测试数据为\n{}'.format(a))


if __name__ == '__main__':
    pytest.main(['-s', 'test_demo.py::TestCases'])
