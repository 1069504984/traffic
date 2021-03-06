__author__ = '程程'
import pymysql
from common.read_conf import ReadConf
from common import project_path
from common.my_log import MyLogg

mylog = MyLogg()


class DoMysql:
    '''查询mysql数据库数据，返回的数据类型根据传入参数的不同而不同'''

    def do_mysql(self, query, flag=1):
        global cursor
        global connection
        global resp
        db_config=ReadConf(project_path.conf_path,"DbConf","db_config").get_data()
        try:
            connection = pymysql.connect(**db_config)
            mylog.my_info("数据库连接成功")
        except Exception as e:
            mylog.my_error("数据库连接失败")
        cursor = connection.cursor()
        cursor.execute(query)
        if flag == 1:
            try:
                resp = cursor.fetchone()  # 返回的数据类型是元祖
                mylog.my_info("数据库查询数据成功，返回数据类型为元组")
            except Exception as e:
                mylog.my_error("数据库获取数据失败")
        else:
            try:
                resp = cursor.fetchall()  # 返回的数据类型是列表里面包含元祖
                mylog.my_info("数据库查询数据成功,返回数据类型为列表嵌套元祖")
            except Exception as e:
                mylog.my_error("数据库获取数据失败")
        return resp


if __name__ == '__main__':
    data = DoMysql().do_mysql("select * from u2s_traffic.camera where name='现场拥堵实时流'", flag=1)
    print(data)
    print((data[0]))
    # # print(int(data["LeaveAmount"]))
    # sql='{"sql_1":"select id from member where mobilephone=15111420847","sql_2":None}'
    #
    # member_id=DoMysql().do_mysql(eval(sql)["sql_1"],1)[0]
    # print(member_id)
    #
    # member_id=DoMysql().do_mysql("select id from member where mobilephone=15111420847",1)[0]
    # print(member_id)
