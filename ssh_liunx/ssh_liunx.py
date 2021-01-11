# -*- coding: utf-8 -*-
# @Time    : 2020/10/16 13:03
# @Author  : Fighter
import paramiko
import time
#所要部署的服务器
host='172.16.1.147'
port=22
#服务器账号密码
username="root"
pwd="root"

class SSHConnection(object):
	#用于连接linux服务器
    def __init__(self, host, port, username, pwd):
        self.host = host
        self.port = port
        self.username = username
        self.pwd = pwd
        self.__k = None
        self.ssh = paramiko.SSHClient()
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.ssh.connect(hostname=self.host, port=self.port, username=self.username, password=self.pwd)
	#输入linux命令并输出结果
    def connect(self,cmd):
        stdin, stdout, stderr = self.ssh.exec_command(cmd)
        result = stdout.read()
        print(str(result,'utf-8'))
        return str(result,'utf-8')
	#关闭linux连接
    def close(self):
        self.ssh.close()


obj = SSHConnection(host,port,username,pwd)
#------------------------停止应用------------------------
#其中app.jar替换成对应需要部署的包名
obj.connect("ps -ef | grep app.jar | grep -v grep | awk '{print $2}' | xargs kill -9 ")
time.sleep(1)