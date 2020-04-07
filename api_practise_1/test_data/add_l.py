# -*- coding: utf-8 -*-
# @Time    : 2020/1/21 16:45
# @Author  : Fighter
class Calculate:
    def __init__(self,num1,num2):
        self.num1 = num1
        self.num2 = num2
    def addition(self):
        result = int(self.num1) + int(self.num2)
        return result

    def subtraction(self):
        result = int(self.num1) - int(self.num2)
        return result

    def multiplication(self):
        result = int(self.num1) * int(self.num2)
        return result

    def division(self):
        if self.num2 == 0:
            return '除数不能为零'
        else:
            result = int(self.num1) / int(self.num2)
            return result