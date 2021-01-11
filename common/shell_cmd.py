# -*- coding: utf-8 -*-
# @Time    : 2020/12/1 14:08
# @Author  : Fighter
import subprocess

"""
执行shell语句的封装
"""

class ComShell:

    def invoke(self, cmd):
        output, errors = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
        result = output.decode("utf-8","ignore")
        return result

if __name__ == '__main__':
    dir="dir"
    cmd = F"{dir}"
    cmd_demo=ComShell()
    result=cmd_demo.invoke(cmd)
    print(result)