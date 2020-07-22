__author__ = '李开'
import pytest
import os

# 生成对应的测试报告
# import unittest
# import HTMLTestRunnerNew
#
# from test_data import task
# from test_data import test_camera
# import  os,sys
# from MakeReport import MakerReport
# curPath = os.path.abspath(os.path.dirname(__file__))
# rootPath = os.path.split(curPath)[0]
# sys.path.append(rootPath)
#
# from  common import project_path
# #新建一个测试集
# suite=unittest.TestSuite()
# #加载测试用例
# loader=unittest.TestLoader()
# suite.addTest(loader.loadTestsFromModule(task))
# suite.addTest(loader.loadTestsFromModule(test_camera))
# # suite.addTest(loader.loadTestsFromModule(login_cases))
# # suite.addTest(loader.loadTestsFromModule(getWarningDetail))
# # suite.addTest(loader.loadTestsFromModule(getserialnumber))
#
# # suite.addTest(loader.loadTestsFromModule(get_FinanceLogList))
# # suite.addTest(loader.loadTestsFromModule(get_loanlist))
# # suite.addTest(loader.loadTestsFromModule(get_InvestsByMemberId))
# # suite.addTest(loader.loadTestsFromModule(get_InvestsByLoanId))
# # suite.addTest(loader.loadTestsFromModule(invest_1_cases))
# # suite.addTest(loader.loadTestsFromModule(register_cases))
# # suite.addTest(loader.loadTestsFromModule(withdraw_cases))
#
# #执行测试用例，生成测试赛报告
# with open(project_path.report_path,"wb") as file:
#     runner=HTMLTestRunnerNew.HTMLTestRunner(stream=file, verbosity=2, title="测试报告第一轮", description="接口自动化测试报告",tester="李开")
#     runner.run(suite)
# # with open(project_path.report_path,"wb") as file:
# #     runner=MakerReport(suite).report(description="任务模块接口流程用例")

if __name__ == '__main__':
    pytest.main(["-v", "--alluredir", "./allure/json", '--clean-alluredir'
                 ])
    os.system("allure generate ./allure/json -o ./allure/html -c")
#  './test_data/test_video.py',
# './test_data/test_camera.py',
#                  './test_data/test_query_task.py',
#                  './test_data/test_add_task.py'
