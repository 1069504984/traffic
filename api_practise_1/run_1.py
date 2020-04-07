# -*- coding: utf-8 -*-
# @Time    : 2020/1/21 16:47
# @Author  : Fighter
import unittest
from test_data.add_l import Calculate


class MyTestCase(unittest.TestCase):
    # 所有的用例都是用test_开头
    def test_addition(self):
        res = Calculate(1,1).addition()
        print('1+1的结果：',res)

    def test_subtraction(self):
        res = Calculate(56,22).subtraction()
        print('56-22的结果：',res)

    def test_multiplication(self):
        res = Calculate(-11,5).multiplication()
        print('-11*5的结果：',res)

    def test_division(self):
        res = Calculate(1,0).division()
        print(r'1\0的结果：',res)





#
#     # unittest.main()  #此方法是按ascii码顺序执行，不是按正常的顺序执行
#     # 方法二：
#     suite = unittest.TestSuite()  #创建一个测试套件,用来存储用例
#     # suite.addTest(MyTestCase('test_addition'))
#     suite.addTest(MyTestCase('test_subtraction'))
#     # suite.addTest(MyTestCase('test_multiplication'))
#     # suite.addTest(MyTestCase('test_division'))
#     runner = unittest.TextTestRunner()
#     runner.run(suite)
