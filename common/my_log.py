'''学习如何自己去定义日志，将测试过程记录到日志中'''
import logging
import os

from common.read_conf import ReadConf
from common import project_path
from common.do_yaml import do_conf_yaml

address = project_path.conf_log_path


class MyLogg:  # 直接写成一个类
    '''专门用来将测试过程写入日志的一个类'''

    def my_lo(self, level, msg):
        my_logger = logging.getLogger(ReadConf(address, "LOG", "new_log_name").get_str())  # 通过配置文件设置日志收集器的名称
        my_logger.setLevel(ReadConf(address, "LOG", "collect_level").get_str())  # 通过配置文件设置日志信息的收集级别
        formatter = logging.Formatter(ReadConf(address, "LOG", "log_formater").get_str())  # 通配置文件设置日志信息的一个输出格式

        ch = logging.StreamHandler()
        ch.setLevel(ReadConf(address, "LOG", "output_level").get_str())  # 通过配置文件设置日志文件的输出级别
        ch.setFormatter(formatter)  # 设置格式
        fl = logging.FileHandler(project_path.log_path, encoding="utf-8")
        fl.setLevel(ReadConf(address, "LOG", "output_level").get_str())  # 设置级别
        fl.setFormatter(formatter)  # 设置格式
        my_logger.addHandler(ch)
        my_logger.addHandler(fl)
        if level == "DEBUG":
            my_logger.debug(msg)
        elif level == "INFO":
            my_logger.info(msg)
        elif level == "WARNING":
            my_logger.warning(msg)
        elif level == "ERROR":
            my_logger.error(msg)
        else:
            my_logger.critical(msg)

        my_logger.removeHandler(ch)
        my_logger.removeHandler(fl)  # 用完之后记得移除

    def my_debug(self, msg):  # 输入debug级别的信息
        self.my_lo("DEBUG", msg)

    def my_info(self, msg):  # 输入info级别的信息
        self.my_lo("info", msg)

    def my_warning(self, msg):  # 输入warning级别的信息
        self.my_lo("WARNING", msg)

    def my_error(self, msg):  # 输入error级别的信息
        self.my_lo("error", msg)

    def my_critical(self, msg):  # 输入critical级别的信息
        self.my_lo("CRITICAL", msg)


class MyLogger(object):

    @classmethod
    def create_logger(cls):
        """创建日志收集器"""
        # 创建一个日志收集器，如果没有传参数，则返回默认日志收集器root
        my_log = logging.getLogger(do_conf_yaml.read("log", "log_name"))
        # 设置日志收集器的收集等级
        my_log.setLevel(do_conf_yaml.read("log", "logger_lever"))

        # 设置日志的输出格式
        formater = logging.Formatter(do_conf_yaml.read("log", "formater"))
        # 日志的输出
        # 创建一个输出到控制台的输出渠道
        sh = logging.StreamHandler()
        sh.setLevel(do_conf_yaml.read("log", "stream_level"))
        # 设置输出到控制台的格式
        sh.setFormatter(formater)
        # 将输出渠道添加到日志收集器中
        my_log.addHandler(sh)
        # 创建一个输出到文件的渠道
        fh = logging.FileHandler(
            filename=os.path.join(project_path.log_dir_path, do_conf_yaml.read("log", "logfile_name")),
            encoding='utf-8')
        fh.setLevel(do_conf_yaml.read("log", "logfile_level"))
        fh.setFormatter(formater)
        my_log.addHandler(fh)

        return my_log


# 创建日志收集器，避免重复调用，日志出现多次
do_log = MyLogger.create_logger()
my_log = MyLogg()

if __name__ == "__main__":
    do_log.error("执行一次")
    my_log.my_warning("111")
