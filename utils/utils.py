# -*- coding: utf-8 -*-
# @Time    : 2020/9/12 12:02
# @Author  : KK
import json

from common.log_demo import logger

def handle_param_type(value):
    """
    处理参数类型
    :param value: 数据
    :return: value数据的类型名
    """
    if isinstance(value, int):
        param_type = "int"
    elif isinstance(value, float):
        param_type = "float"
    elif isinstance(value, bool):
        param_type = "boolean"
    else:
        param_type = "string"

    return param_type


def handle_data1(datas):
    """
    处理第一种类型的数据转化
    将[{'check': 'status_code', 'expected':200, 'comparator': 'equals'}]
    转化为 [{key: 'status_code', value: 200, comparator: 'equals', param_type: 'string'}],
    :param datas: 待转换的参数列表
    :return:
    """
    result_list = []
    if datas is not None:
        for one_validate_dict in datas:
            key = one_validate_dict.get("check")
            value = one_validate_dict.get("expected")
            comparator = one_validate_dict.get("comparator")
            result_list.append({
                "key": key,
                "value": value,
                "comparator": comparator,
                "param_type": handle_param_type(value)
            })

    return result_list

def query_json( json_content, query, delimiter='.'):
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
# response=query_json(json_content,query="person.name.first_name.2")
# print(response) # 输出结果 str -> o



def get_uniform_comparator(comparator):
    """ convert comparator alias to uniform name
    """
    if comparator in ["eq", "equals", "==", "is"]:
        return "equals"
    elif comparator in ["lt", "less_than"]:
        return "less_than"
    elif comparator in ["le", "less_than_or_equals"]:
        return "less_than_or_equals"
    elif comparator in ["gt", "greater_than"]:
        return "greater_than"
    elif comparator in ["ge", "greater_than_or_equals"]:
        return "greater_than_or_equals"
    elif comparator in ["ne", "not_equals"]:
        return "not_equals"
    elif comparator in ["str_eq", "string_equals"]:
        return "string_equals"
    elif comparator in ["len_eq", "length_equals", "count_eq"]:
        return "length_equals"
    elif comparator in ["len_gt", "count_gt", "length_greater_than", "count_greater_than"]:
        return "length_greater_than"
    elif comparator in ["len_ge", "count_ge", "length_greater_than_or_equals", \
        "count_greater_than_or_equals"]:
        return "length_greater_than_or_equals"
    elif comparator in ["len_lt", "count_lt", "length_less_than", "count_less_than"]:
        return "length_less_than"
    elif comparator in ["len_le", "count_le", "length_less_than_or_equals", \
        "count_less_than_or_equals"]:
        return "length_less_than_or_equals"
    else:
        return comparator

class Context(object):
    """ Manages context functions and variables.
        context has two levels, testset and testcase.
    """
    def __init__(self):
        self.init_context()

    def init_context(self, level='testset'):
        """
        testset level context initializes when a file is loaded,
        testcase level context initializes when each testcase starts.
        """
        if level == "testset":
            self.testset_functions_config = {}
            self.testset_request_config = {}


    def eval_content(self, content):
        """ evaluate content recursively, take effect on each variable and function in content.
            content may be in any data structure, include dict, list, tuple, number, string, etc.
        """
        return json.loads(content)

    def collection_get(self,obj, attr, default=None):
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
    def eval_check_item(self, validator, resp_obj):
        """ evaluate check item in validator
        @param (dict) validator
            {"check": "status_code", "comparator": "eq", "expect": 201}
            {"check": "$resp_body_success", "comparator": "eq", "expect": True}
        @param (object) resp_obj
        @return (dict) validator info
            {
                "check": "status_code",
                "check_value": 200,
                "expect": 201,
                "comparator": "eq"
            }
        """
        check_item = validator["check"]
        # check_item should only be the following 5 formats:
        # 1, variable reference, e.g. $token
        # 2, function reference, e.g. ${is_status_code_200($status_code)}
        # 3, dict or list, maybe containing variable/function reference, e.g. {"var": "$abc"}
        # 4, string joined by delimiter. e.g. "status_code", "headers.content-type"
        # 5, regex string, e.g. "LB[\d]*(.*)RB[\d]*"

        if isinstance(check_item, (dict, list)):
            check_value = self.collection_get(
                resp_obj,check_item,default=None)

        validator["check_value"] = check_value
        expect_value = self.eval_content(validator["expect"])
        validator["expect"] = expect_value
        return validator



    def validate(self, validators, resp_obj):
        """ make validations
        """
        if not validators:
            return

        logger.info("start to validate.")
        self.evaluated_validators = []
        for validator in validators:
            # evaluate validators with context variable mapping.
            evaluated_validator = self.eval_check_item(
                validator, resp_obj
            )
            self.evaluated_validators.append(evaluated_validator)
