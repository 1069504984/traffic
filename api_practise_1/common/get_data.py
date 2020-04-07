__author__ = '程程'
#学习如何利用反射来完成多个请求之间数据的传递，比如cookies的传递
from  common.read_conf import ReadConf
from  common import project_path
from  common.my_log import MyLogg
mylog=MyLogg()
import re
class GetData:
    """
    用来动态的存储 修改 删除 添加 数据以及参数化数据
    利用re+反射，进行查找需要替换的参数，通过反射拿到对应的值
    """
    COOKIES=None

    loan_id=2#新添加标的id 初始值
    normal_user=ReadConf(project_path.conf_path,"CaseData","normal_user").get_str()
    normal_pwd=ReadConf(project_path.conf_path,"CaseData","normal_pwd").get_str()
    normal_member_id=None
    max_id=ReadConf(project_path.conf_path,"CaseData","max_id").get_str()
    # normal_member_id=ReadConf(project_path.conf_path,"CaseData","normal_member_id").get_str()
    def replace(self,target):
        p_2="#(.*?)#"
        while re.search(p_2,target):
            m=re.search(p_2,target)
            key=m.group(1)
            try:
                value=getattr(GetData,key)
                mylog.my_info("参数化的数据是：{}".format(value))
            except Exception as e:
                mylog.my_error("参数化失败")
                raise e
            target=re.sub(p_2,value,target,count=1)
        return target


if __name__ == '__main__':
    print(GetData().max_id)
    data='{"sql_1":None,"sql_2":"select #max_id# from loan","sql_3":None}'
    data=GetData().replace(data)
    print(data)







