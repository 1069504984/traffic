__author__ = '程程'
# 文件的路径放到这里
import os

project_path = os.path.split(os.path.split(os.path.realpath(__file__))[0])[0]  # 获取目前文件的路径
# 测试用例的路径
case_path = os.path.join(project_path, "test_data", "test_case.xlsx")
exampels_path = os.path.join(project_path, "test_examples", "jkcs.xlsx")

# 2测试报告的路径
report_path = os.path.join(project_path, "test_result", "test_report", "test_1.html")

# 3日志输出文件的路径
log_path = os.path.join(project_path, "test_result", "test_log", "cs.log")

# 4配置文件的路径
conf_path = os.path.join(project_path, "conf", "case.conf")
conf_log_path = os.path.join(project_path, "conf", "log.conf")
if __name__ == '__main__':
    print(conf_log_path)
