# -*- coding: utf-8 -*-
# @Time    : 2020/7/22 9:45
# @Author  : Fighter
import yaml
from common import project_path


class HandleYaml(object):
    def __init__(self, filename):
        self.filename = filename

    def read(self, section, option):
        with open(self.filename, mode='r', encoding='utf-8') as file:
            datas = yaml.load(file, Loader=yaml.FullLoader)
            return datas[section][option]

    @staticmethod  # 独立的，没使用class的方法，filename跟读方法分开
    def write(datas, filename):
        with open(filename, mode='w', encoding='utf-8') as file:
            yaml.dump(datas, file, allow_unicode='utf-8')


do_conf_yaml = HandleYaml(project_path.yaml_conf_path)

if __name__ == '__main__':
    datas = {
        "peopleMsg": {"name": "leon"},
        "peopleScore": {"math": 95, "english": 120}
    }
    do_conf_yaml.write(datas, project_path.yaml_conf_path)