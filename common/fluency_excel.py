# -*- coding: utf-8 -*-
# @Time    : 2020/7/29 14:28
# @Author  : Fighter
import openpyxl
import os
from common import project_path


class DataCase(object):
    pass


class HandleExcel(object):

    def __init__(self, sheetname, filename=None):
        if filename is None:
            self.filename = project_path.test_case_path
        else:
            self.filename = filename
        self.sheetname = sheetname

    def open(self):
        self.wb = openpyxl.load_workbook(self.filename)
        self.sh = self.wb[self.sheetname]

    def read_data(self):
        self.open()
        rows = list(self.sh.rows)
        # 创建空列表存储用例数据
        cases = []
        title_sh = [i.value for i in rows[0]]

        for r in rows[1:]:
            data = [i.value for i in r]
            # 创建用例数据对象
            case = DataCase()
            for c in zip(title_sh, data):
                setattr(case, c[0], c[1])
            cases.append(case)
            self.wb.close()
        return cases

    def write_data(self, row, column, value):
        self.open()
        self.sh.cell(row=row, column=column, value=value)
        self.wb.save(self.filename)
        self.wb.close()


if __name__ == '__main__':
    test_case = HandleExcel("camera").read_data()
    print(dir(test_case[0]))
