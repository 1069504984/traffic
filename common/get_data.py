__author__ = '李开'
# 学习如何利用反射来完成多个请求之间数据的传递，比如cookies的传递
from common.read_conf import ReadConf
from common import project_path
from common.log_demo import logger

# logger = loggerg()
from common.do_mysql import DoMysql
import jsonpath
import re


class GetData:
    """
    用来动态的存储 修改 删除 添加 数据以及参数化数据
    利用re+反射，进行查找需要替换的参数，通过反射拿到对应的值
    正则替换需要都是str
    """
    COOKIES = None
    token = None
    max_id = ReadConf(project_path.conf_path, "CaseData", "max_id").get_str()
    cameraId = ReadConf(project_path.conf_path, "CaseData", "cameraId").get_str()  # 监控点id
    sceneId = ReadConf(project_path.conf_path, "CaseData", "sceneId").get_str()
    name = repr(ReadConf(project_path.conf_path, "CaseData", "name").get_str())  # 监控点名称
    sql_name = ReadConf(project_path.conf_path, "CaseData", "name").get_str()
    serialnumber = str(ReadConf(project_path.conf_path, "CaseData", "serialnumber").get_str())
    update_name = repr(ReadConf(project_path.conf_path, "CaseData", "update_name").get_str())
    sql_update_name = ReadConf(project_path.conf_path, "CaseData", "update_name").get_str()

    Max_serialnumber = str(DoMysql().do_mysql("SELECT max(serialnumber) FROM u2s.vsd_task", 1)[0])
    Max_cameraId = str(DoMysql().do_mysql("SELECT max(id) FROM u2s_traffic.camera", 1)[0])
    fileId = None

    # cameraFileId=str(DoMysql().do_mysql("SELECT id FROM u2s_traffic.ctrl_unit_file where file_name = 'test_video.mp4'",1)[0])
    cameraFileId = None

    def replace(self, target):
        p_2 = "#(.*?)#"
        while re.search(p_2, target):
            m = re.search(p_2, target)
            key = m.group(1)
            if len(key) < 20:
                try:
                    value = getattr(GetData, key)
                    logger.info("参数化的数据是：{}".format(value))
                except Exception as e:
                    logger.error("参数化失败")
                    raise e
                target = re.sub(p_2, value, target, count=1)
            else:
                break
        return target

    @staticmethod
    def get_json_value(json_data, key0, key1=None, key2=None, num=None, type=None):
        '''获取到json中任意key的值,结果为list格式'''
        if type == None:
            key_value = jsonpath.jsonpath(json_data, '$..{key0}'.format(key0=key0))
        elif type == 2:
            key_value = jsonpath.jsonpath(json_data, '$.{key0}.{key1}'.format(key0=key0, key1=key1))
        elif type == "lt":
            key_value = jsonpath.jsonpath(json_data, F'$..{key0}[?(@.{key1}<{num})]')
        elif type == "gt":
            key_value = jsonpath.jsonpath(json_data,
                                          '$..{key0}[?(@.{key1}>{num})]'.format(key0=key0, key1=key1,
                                                                                num=num))
        # key的值不为空字符串或者为empty（用例中空固定写为empty）返回对应值，否则返回empty

        return key_value


if __name__ == '__main__':
    json = {
        "store": {
            "book": [
                {
                    "category": "reference",
                    "book": "Nigel Rees",
                    "title": "Sayings of the Century",
                    "price": 8.95
                },
                {
                    "category": "fiction",
                    "author": "Evelyn Waugh",
                    "title": "Sword of Honour",
                    "price": 12.99
                },
                {
                    "category": "fiction",
                    "author": "Herman Melville",
                    "title": "Moby Dick",
                    "isbn": "0-553-21311-3",
                    "price": 8.99
                },
                {
                    "category": "fiction",
                    "author": "J. R. R. Tolkien",
                    "title": "The Lord of the Rings",
                    "isbn": "0-395-19395-8",
                    "price": 22.99
                }
            ],
            "bicycle": {
                "color": "red",
                "price": 19.95
            }
        },
        "expensive": 10}
    print(GetData.get_json_value(json, "book"))
    print(jsonpath.jsonpath(json, '$..book[?(@.price<10)]'))
    print(GetData.get_json_value(json, key0="book", key1="price", num=10, type="gt"))
