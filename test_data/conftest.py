# -*- coding: utf-8 -*-
# @Time    : 2020/4/26 14:52
# @Author  : Fighter
# import json
# import time
# import requests
# from common.do_mysql import DoMysql
# from common.do_requests import DoRequests
# from common.learn_do_excel import DoExcel
# from common import project_path
# from common import get_data
# from common.log_demo import logger
# import pytest
#
#
#
#
# @pytest.fixture()
# def test_login():
#     test_data = DoExcel(project_path.test_case_path, "camera").read_data()[0]
#     test_result = DoRequests(test_data["url"],
#                              test_data["method"],
#                              test_data["param"]).request(headers=eval(test_data["header"]),
#                                                          cookies=getattr(get_data.GetData,
#                                                                          "COOKIES"))
#     if test_result.cookies:  # 判断请求cookies是否为空
#         cookies = requests.utils.dict_from_cookiejar(test_result.cookies)
#         setattr(get_data.GetData, "COOKIES", cookies)
#     print("登录成功")
#
#
# @pytest.fixture(scope="class")
# def add_camera_task():
#     test_data = DoExcel(project_path.test_case_path, "video").read_data()[0]
#     test_result = DoRequests(test_data["url"],
#                              test_data["method"],
#                              test_data["param"]).request(headers=eval(test_data["header"]),
#                                                          cookies=getattr(get_data.GetData,
#                                                                          "COOKIES"))
#     if test_result.cookies:
#         cookies = requests.utils.dict_from_cookiejar(test_result.cookies)
#         setattr(get_data.GetData, "COOKIES", cookies)
#     logger.info("登录成功--------------后续执行添加监控点")
#     test_data1 = DoExcel(project_path.test_case_path, "video").read_data()[1]
#     DoRequests(test_data1["url"],
#                test_data1["method"],
#                get_data.GetData().replace(test_data1["param"]).encode("utf-8")).request(
#         headers=eval(test_data1["header"]),
#         cookies=getattr(get_data.GetData,
#                         "COOKIES"))
#     sql = test_data1["sql"]
#     print(sql)
#     if sql is not None:
#         sql = get_data.GetData().replace(sql)
#     if sql is not None and eval(sql)["sql_1"]:
#         cameraId = DoMysql().do_mysql(eval(sql)["sql_1"], 1)[0]
#         setattr(get_data.GetData, 'cameraId', str(cameraId))
#     logger.info("监控点步骤完成----------------后续执行添加视频")
#
#     test_data3 = DoExcel(project_path.test_case_path, "video").read_data()[2]
#     qurey_cameraid = "SELECT id FROM u2s_traffic.camera WHERE name='测试test'"
#     cameraid = DoMysql().do_mysql(qurey_cameraid)[0]
#     test_result3 = DoRequests(test_data3["url"], test_data3["method"],
#                               eval(get_data.GetData().replace(str(eval(test_data3["param"])[0]))),
#                               files=eval(test_data3["param"])[-1]).request(headers=eval(test_data3["header"]),
#                                                                            cookies=getattr(get_data.GetData,
#                                                                                            "COOKIES"))
#     filename = repr(eval(test_data3["param"])[-1].get('filename'))
#     qurey_fileid = "SELECT id FROM u2s_traffic.ctrl_unit_file WHERE camera_id={} and file_name={}".format(
#         cameraid, filename)
#     fileid = DoMysql().do_mysql(qurey_fileid)[0]
#     setattr(get_data.GetData, "cameraFileId", str(fileid))
#     setattr(get_data.GetData, "cameraId", str(cameraid))
#     time.sleep(15)
#     logger.info("添加视频完成-------------------------后续执行添加结构化任务")
#
#     test_data4 = DoExcel(project_path.test_case_path, "add_task").read_data()[2]
#     test_result4 = DoRequests(test_data4["url"],
#                               test_data4["method"],
#                               get_data.GetData().replace(test_data4["param"]).encode("utf-8")).request(
#         headers=eval(test_data4["header"]),
#         cookies=getattr(get_data.GetData,
#                         "COOKIES"))
#     try:
#         if "data" in test_result4.json() and test_result4.json()["data"] is not None and len(
#                 test_result4.json()["data"]) == 19:
#             setattr(get_data.GetData, "serialnumber", test_result4.json()["data"])
#             print("需要删除的任务号为:{}".format(getattr(get_data.GetData, "serialnumber")))
#     except Exception as e:
#         print("res有误，请check数据，{}".format(e))
#     yield
#     print("测试前置完成，开始数据清理")
#     test_data5 = DoExcel(project_path.test_case_path, "clean").read_data()[0]
#     test_result5 = DoRequests(test_data5["url"],
#                               test_data5["method"],
#                               eval(get_data.GetData().replace(test_data5["param"]))).request(
#         headers=eval(test_data5["header"]),
#         cookies=getattr(get_data.GetData,
#                         "COOKIES"))
#     print(json.dumps(test_result5.json(), indent=3))
#     logger.info("数据清理完毕---------------------------")
