# 如何读取配置文件里面的数据
from configparser import ConfigParser

'''引入一个专门进行读取配置文件的类'''


# cf=ConfigParser()
# cf.read(r"C:\Users\程程\PycharmProjects\learn_python_1\learn_python_1\pzwj.conf",encoding="utf-8")#read()里面放的是配置文件的地址名,记得加入转码
# data=cf.get("Time","nowday")#get函数是有返回值的
# print(data)

class ReadConf:
    '''一个用来转门读取配置文件的类'''

    def __init__(self, filename, setion, option):
        self.cf = ConfigParser()  # 在类中创造了一个公用的对象
        try:
            self.cf.read(filename, encoding="utf-8")  # 在调用类的时候就帮你把数据读取好了，只需要你去获取
        except Exception as e:
            raise e
        self.setion = setion
        self.option = option

    def get_int(self):
        '''获取数据类型为整数型的数据'''
        try:
            data = self.cf.getint(self.setion, self.option)
            return data
        except Exception as e:
            raise e

    def get_float(self):
        '''获取数据类型为浮点型的数据'''
        try:
            data = self.cf.getfloat(self.setion, self.option)
            return data
        except Exception as e:
            raise e

    def get_boolean(self):
        '''获取数据类型为布尔型的数据'''
        try:
            data = self.cf.getboolean(self.setion, self.option)
            return data
        except Exception as e:
            raise e

    def get_str(self):  # get()方法默认返回的数据类型是字符串
        '''获取数据类型为字符串类型的数据'''
        try:
            data = self.cf.get(self.setion, self.option)
            return data
        except Exception as e:
            raise e

    def get_data(self):
        '''获取数据类型为列表，元祖，字典的数据'''
        try:
            data = self.cf.get(self.setion, self.option)
            return eval(data)
        except Exception as e:
            raise e


if __name__ == '__main__':
    from common import project_path

    db_config = ReadConf(project_path.conf_path, "DbConf", "db_config").get_data()
    print(db_config)
