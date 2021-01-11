'''学习如何自己去定义日志，将测试过程记录到日志中'''
import logging
import os
import sys
from common.read_conf import ReadConf
from common import project_path
from common.do_yaml import do_conf_yaml

address = project_path.conf_log_path


class MyLogg:  # 直接写成一个类
    '''专门用来将测试过程写入日志的一个类'''

    def logger(self, level, msg):
        loggerger = logging.getLogger(ReadConf(address, "LOG", "new_log_name").get_str())  # 通过配置文件设置日志收集器的名称
        loggerger.setLevel(ReadConf(address, "LOG", "collect_level").get_str())  # 通过配置文件设置日志信息的收集级别
        formatter = logging.Formatter('%(asctime)s - %(name)s - "%(pathname)s:%(lineno)d" - %(funcName)s - %(levelname)s - %(message)s',
            "%Y-%m-%d %H:%M:%S")  # 通配置文件设置日志信息的一个输出格式
        ch = logging.StreamHandler()
        ch.setLevel(ReadConf(address, "LOG", "output_level").get_str())  # 通过配置文件设置日志文件的输出级别
        ch.setFormatter(formatter)  # 设置格式
        fl = logging.FileHandler(project_path.log_path, encoding="utf-8")
        fl.setLevel(ReadConf(address, "LOG", "output_level").get_str())  # 设置级别
        fl.setFormatter(formatter)  # 设置格式
        loggerger.addHandler(ch)
        loggerger.addHandler(fl)
        if level == "debug":
            loggerger.debug(msg)
        elif level == "info":
            loggerger.info(msg)
        elif level == "WARNING":
            loggerger.warning(msg)
        elif level == "error":
            loggerger.error(msg)
        else:
            loggerger.critical(msg)

        loggerger.removeHandler(ch)
        loggerger.removeHandler(fl)  # 用完之后记得移除

    def my_debug(self, msg):  # 输入debug级别的信息
        self.logger("debug", msg)

    def info(self, msg):  # 输入info级别的信息
        self.logger("info", msg)

    def warning(self, msg):  # 输入warning级别的信息
        self.logger("WARNING", msg)

    def error(self, msg):  # 输入error级别的信息
        self.logger("error", msg)

    def my_critical(self, msg):  # 输入critical级别的信息
        self.logger("CRITICAL", msg)


class MyLogger(object):

    @classmethod
    def create_logger(cls):
        """创建日志收集器"""
        # 创建一个日志收集器，如果没有传参数，则返回默认日志收集器root
        logger = logging.getLogger(do_conf_yaml.read("log", "log_name"))
        # 设置日志收集器的收集等级
        logger.setLevel(do_conf_yaml.read("log", "logger_lever"))

        # 设置日志的输出格式
        formater = logging.Formatter(do_conf_yaml.read("log", "formater"))
        # 日志的输出
        # 创建一个输出到控制台的输出渠道
        sh = logging.StreamHandler()
        sh.setLevel(do_conf_yaml.read("log", "stream_level"))
        # 设置输出到控制台的格式
        sh.setFormatter(formater)
        # 将输出渠道添加到日志收集器中
        logger.addHandler(sh)
        # 创建一个输出到文件的渠道
        fh = logging.FileHandler(
            filename=os.path.join(project_path.log_dir_path, do_conf_yaml.read("log", "logfile_name")),
            encoding='utf-8')
        fh.setLevel(do_conf_yaml.read("log", "logfile_level"))
        fh.setFormatter(formater)
        logger.addHandler(fh)

        return logger








# # 创建日志收集器，避免重复调用，日志出现多次
# do_log = MyLogger.create_logger()
# logger = MyLogg()
