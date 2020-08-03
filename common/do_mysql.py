__author__ = '程程'
import pymysql
from common.read_conf import ReadConf
from common import project_path
from common.log_demo import logger




class DoMysql:
    '''查询mysql数据库数据，返回的数据类型根据传入参数的不同而不同'''

    def do_mysql(self, query, flag=1, type=None):
        global cursor
        global connection
        global resp
        # db_config=ReadConf(project_path.conf_path,"DbConf","dev_db_config").get_data()
        db_config = ReadConf(project_path.conf_path, "DbConf", "test_db_config").get_data()
        try:
            connection = pymysql.connect(**db_config)
        except Exception as e:
            logger.error("数据库连接失败")
        cursor = connection.cursor()
        cursor.execute(query)
        if type == "insert":
            try:
                connection.commit()
                logger.info("插入语句{}成功".format(query))
            except Exception as e:
                print(e)
        if flag == 1:
            try:
                resp = cursor.fetchone()  # 返回的数据类型是元祖
                # logger.info("数据库查询数据成功，返回数据为{}".format(resp))
            except Exception as e:
                logger.error("数据库获取数据失败")
        else:
            try:
                resp = cursor.fetchall()  # 返回的数据类型是列表里面包含元祖
                # logger.info("数据库查询数据成功,返回数据类型为列表嵌套元祖")
            except Exception as e:
                logger.error("数据库获取数据失败")
        connection.close()
        return resp


if __name__ == '__main__':
    pass
    # data = DoMysql().do_mysql("SELECT * FROM `vsd_task_info`  where from_type=3 LIMIT 0, 10", flag=2)
    # print(data)
    # print(type(data))
    # print(len(data))
    # print((data[0]))
    # # print(int(data["LeaveAmount"]))
    # sql='{"sql_1":"select id from member where mobilephone=15111420847","sql_2":None}'
    #
    # member_id=DoMysql().do_mysql(eval(sql)["sql_1"],1)[0]
    # print(member_id)
    #
    # member_id=DoMysql().do_mysql("select id from member where mobilephone=15111420847",1)[0]
    # print(member_id)
