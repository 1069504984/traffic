__author__ = '程程'
# 文件的路径放到这里
import os

project_path = os.path.dirname((os.path.dirname(os.path.abspath(__file__))))# 获取目前文件的路径
# 测试用例的路径
test_case_path = os.path.join(project_path, "excel_data", "test_case_107.xlsx")
dev_case_path = os.path.join(project_path, "excel_data", "test_case_129.xlsx")
# 2测试报告的路径
report_path = os.path.join(project_path, "test_result", "test_report")

# 3日志输出文件的路径
log_dir_path = os.path.join(project_path, "test_result", "test_log")
log_path = os.path.join(project_path, "test_result", "test_log", "cs.log")
log_dir_path = os.path.join(project_path, "test_result", "test_log")

# 4配置文件的路径
conf_path = os.path.join(project_path, "conf", "case.conf")
conf_log_path = os.path.join(project_path, "conf", "log.conf")
yaml_conf_path = os.path.join(project_path, 'conf', 'confyml.yaml')
if __name__ == '__main__':
    print(project_path)
    print(conf_log_path)
