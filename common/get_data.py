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
    normal_user = str(1)
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

def query_json(json_content, query, delimiter='.'):
    """ Do an xpath-like query with json_content.
    @param (dict/list/string) json_content
        json_content = {
            "ids": [1, 2, 3, 4],
            "person": {
                "name": {
                    "first_name": "Leo",
                    "last_name": "Lee",
                },
                "age": 29,
                "cities": ["Guangzhou", "Shenzhen"]
            }
        }
    @param (str) query
        "person.name.first_name"  =>  "Leo"
        "person.name.first_name.0"  =>  "L"
        "person.cities.0"         =>  "Guangzhou"
    @return queried result
    """
    raise_flag = False
    response_body = u"response body: {}\n".format(json_content)
    # 如果提取响应值属性失败，用户可提供一个值，用户值可带在提取路径后，以冒号接在提取后
    # 如："person.name.first_name.0:no first"  =>  "L"
    # 用户提供的取值只能是字串类型，应对一般接口的情况是够用了
    # 如果要提取空串作为错误值，直接写冒号即可
    query_list = query.split(':')
    query = query_list[0]
    basestring = (str, bytes)
    try:
        for key in query.split(delimiter):
            if isinstance(json_content, (list, basestring)):
                json_content = json_content[int(key)]
            elif isinstance(json_content, dict):
                json_content = json_content[key]
            else:
                logger.error(
                    "invalid type value: {}({})".format(json_content, type(json_content)))
                raise_flag = True
    except (KeyError, ValueError, IndexError):
        if len(query_list) == 1:
            # 如果此列表长度为1，即说明用户未提供错误值，可报错
            raise_flag = True
        else:
            json_content = query_list[1]

    if raise_flag:
        err_msg = u"Failed to extract! => {}\n".format(query)
        err_msg += response_body
        logger.error(err_msg)


    return json_content

def collection_get(obj, attr, default=None):
    """
    从复杂的数据结构中提取字段数据
    :param obj: 数据
    :param attr: 字段路径, 列表/数组使用索引,字典使用key,多层路径以点连接.
    :param default:取值失败时,返回的默认值
    :return:字段数据
    """
    try:
        if '.' in attr:
            attr_path = attr.split('.')
            for a in attr_path:
                obj = obj[int(a)] if str.isdigit(a) else obj.get(a)
                # 如果obj为None,则当前a是不存在的key
                if obj is None:
                    raise Exception('路径错误,{}不存在'.format(a))
            # 遍历到最后,此即为目标取值
            return obj
        else:
            return obj[int(attr)] if str.isdigit(attr) else obj.get(attr, default)
    except Exception as e:
        logger.error('数据获取失败，{}'.format(e))
        return default or str(e)
if __name__ == '__main__':
    # json_content = {
    #             "ids": [1, 2, 3, 4],
    #             "person": {
    #                 "name": {
    #                     "first_name": "Leo",
    #                     "last_name": "Lee",
    #                 },
    #                 "age": 29,
    #                 "cities": ["Guangzhou", "Shenzhen"]
    #             }
    #         }
    # response=collection_get(json_content,attr="perso",default=3)
    # print(response)
    target="#sql_name#"
    a=GetData().replace(target)
    print(a)
# response=query_json(json_content,query="person.name.first_name.2")
# print(response) # 输出结果 str -> o



