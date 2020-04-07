__author__ = '程程'
#正则表达式学习
'''

学习正则表达式的草稿练习
'''
from  common.read_conf import ReadConf
from  common import project_path
from  common import get_data
import re
str_1='{"mobilephone":"#normal_user#","pwd":"#normal_pwd#"}'
# p="mobilephone"#原义字符的查找
p_2="#(.*?)#"   #圆括号代表正则中组的概念
# object=re.search(p_2,str_1)#第一参数是查找替换的字符串，第二个是寻找的目标字符串，第三个是寻找到之后替换的次数
# print(object)
# print(object.group())#不传参的时候返回表达式和匹配字符串一起
# print(object.group(1))#传参返回符合正则表达式的字符串
# mm=re.findall(p_2,str_1)#finaall返回所有符合正则的字符串，用列表包起来
# print(mm)#返回一个列表，里面包含所有符合正则表达式的字符串
# target=re.sub(p_2,ReadConf(project_path.conf_path,"CaseData","normal_user").get_str(),str_1,count=1)
# print(target)
# target_1=re.sub(p_2,ReadConf(project_path.conf_path,"CaseData","normal_pwd").get_str(),target,count=1)
# print(target_1)

while re.search(p_2,str_1):
    m=re.search(p_2,str_1)
    key=m.group(1)
    value=getattr(get_data.GetData,key)
    print(type(value))
    print("数据是{}".format(value))
    str_1=re.sub(p_2,value,str_1,count=1)
print(type(str_1))
