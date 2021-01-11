# -*- coding: utf-8 -*-
# @Time    : 2020/10/16 11:20
# @Author  : Fighter
from jenkins import Jenkins


# 创建 Jenkins实例的 handle
api_token = "11da3e59ff3e9832abccbc8c240ae10cb0"
jen = Jenkins(url="http://172.16.1.51:8080/", username="lsptest", password=api_token)

job_name = "TZAPI_test"

# 返回job的个数
# jen.jobs_count()
# 返回所有的job，列表格式
# jen.get_jobs()
# print(jen.get_jobs())
# jen.get_all_jobs()

# 返回job信息，字典格式
# print(jen.get_job_info(name=job_name))

# 返回名字匹配的job的信息，列表格式
# pattern = "^jen"
# jen.get_job_info_regex(pattern=pattern)

# 返回job信息，易阅读的格式
# print(jen.debug_job_info(job_name=job_name))

# 返回 HTTP 响应体 ，字符串形式
# url = "http://148.70.212.152:9090/job/2048test/"
# jen.jenkins_open(req=url)

# 返回第n次构建信息，字典格式
# n = 1
# jen.get_build_info(name=job_name, number=n)

# 返回第n次构建环境变量
# jen.get_build_env_vars(name=job_name, number=n)

# 返回第n次测试报告
# print(jen.get_build_test_report(name=job_name, number=620))

# 返回所以job信息字典，字典格式
# jen.get_queue_info()

# 取消队列中的某个构建
# jen.cancel_queue(id=n)

# 返回当前用户账号信息， 字典格式
# print(jen.get_whoami())

# 返回版本信息， 字符串格式
# print(jen.get_version())

# 返回所有已安装的插件信息，列表格式
# jen.get_plugins()

# 返回某个插件的信息，字典格式
# jen.get_plugin_info(name="插件名字")

# 复制一个jenkins任务
new_name = "new_job"
# jen.copy_job(from_name=job_name, to_name=new_name)

# 重命名一个job
# jen.rename_job(from_name=job_name, to_name=new_name)

# 删除一个job
# jen.delete_job(name=job_name)

# 启用一个job
# jen.enable_job(name=job_name)

# 禁止一个job
# jen.disable_job(name=job_name)

# 设置下次构建的序号
# jen.set_next_build_number(name=job_name, number=n)

# 判断job是否存在
# jen.job_exists(name=job_name)

# 创建一个job
# jen.create_job(name=job_name, config_xml="配置信息xml字符串格式")

# 获取job的配置
# print("配置列: ",jen.get_job_config(name=job_name))

# 重新配置Job
# jen.reconfig_job(name=job_name, config_xml="配置信息xml字符串格式")

# 出发构建job
# parameters = "参数，默认为None"
# print(jen.build_job(name=job_name, parameters=None))

# 安装插件
# jen.install_plugin(name="插件名字")

# 停止正在运行的jenkins构建
print(jen.stop_build(name=job_name, number=622))

# 删除构建
# jen.delete_build(name=job_name, number=n)

# 获取正在运行的构建
print(jen.get_running_builds())