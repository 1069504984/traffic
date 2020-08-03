# -*- coding: utf-8 -*-
# @Time    : 2020/8/3 10:08
# @Author  : Fighter
from common import project_path
from nb_log import LogManager

logger = LogManager('Traffic').get_logger_and_add_handlers(log_path=project_path.log_dir_path, log_filename="cs.log")
