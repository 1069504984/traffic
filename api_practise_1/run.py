__author__ = '程程'
#生成对应的测试报告
import unittest
import HTMLTestRunnerNew
from  test_data import login_cases
from  test_data import test_get
from  test_data import generate_repayments
from  test_data import getWarningDetail
from  test_data import get_InvestsByLoanId
from  test_data import get_InvestsByMemberId
from  test_data import get_loanlist
from  test_data import invest_1_cases
from  test_data import deatil_cases
from  test_data import register_cases
from  test_data import withdraw_cases

from  common import project_path
#新建一个测试集
suite=unittest.TestSuite()
#加载测试用例
loader=unittest.TestLoader()
# suite.addTest(loader.loadTestsFromModule(login_cases))
suite.addTest(loader.loadTestsFromModule(getWarningDetail))
suite.addTest(loader.loadTestsFromModule(test_get))
# suite.addTest(loader.loadTestsFromModule(generate_repayments))
# suite.addTest(loader.loadTestsFromModule(get_FinanceLogList))
# suite.addTest(loader.loadTestsFromModule(get_loanlist))
# suite.addTest(loader.loadTestsFromModule(get_InvestsByMemberId))
# suite.addTest(loader.loadTestsFromModule(get_InvestsByLoanId))
# suite.addTest(loader.loadTestsFromModule(invest_1_cases))
# suite.addTest(loader.loadTestsFromModule(register_cases))
# suite.addTest(loader.loadTestsFromModule(withdraw_cases))

#执行测试用例，生成测试赛报告
with open(project_path.report_path,"wb") as file:
    runner=HTMLTestRunnerNew.HTMLTestRunner(stream=file, verbosity=2, title="测试报告第一轮", description="接口自动化测试报告",tester="李开")
    runner.run(suite)


