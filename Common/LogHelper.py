import logging
import datetime
import os
import inspect
import pdb
from collections import defaultdict
from Entitys.DbLog import LogStack
import Common.UtilKit
class FLLog():
	logger=None
	def __init__(self):
		if not self.logger:
			logger = logging.getLogger('mylogger')
			logger.setLevel(logging.DEBUG)
			# 创建一个handler，用于写入日志文件
			mdpt=inspect.getmodule(self).__file__
			fdpt='{0}/../Logger'.format(os.path.split(mdpt)[0])
			if not os.path.exists(fdpt):
				os.mkdir(fdpt)
			fh = logging.FileHandler('Log{1:%Y-%m-%d}.log')
			fh.setLevel(logging.DEBUG)
			# 再创建一个handler，用于输出到控制台 
			ch = logging.StreamHandler()
			ch.setLevel(logging.DEBUG)
			# 定义handler的输出格式
			formatter = logging.Formatter('''
-------------------------------------------------------
LogTime:%(asctime)s
LogLeve:%(levelname)s
LogName:%(name)s
CallPath:%(funcName)s
LogMessage:%(message)s
''')
			fh.setFormatter(formatter)
			ch.setFormatter(formatter)
			# 给logger添加handler 
			logger.addHandler(fh)
			logger.addHandler(ch)
			FLLog.logger=logger
	def WriteLog(self,message):
		FLog.logger.info(message)
	def WriteErr(self,message):
		FLog.logger.error(message)
	def WriteWar(self,message):
		FLog.logger.warning(message)
class DBLog():
	def WriteLog(self,Message,ClassName=None,MethodName=None,FileLine=None,Leve=1,Result=None,TimeSpans=None,CreatedBy=None,CreatedTime=None):
		cfargs=inspect.getargvalues(inspect.currentframe())
		argpec=[{'key':key,'value':value} for key,value in cfargs.locals.items() if key in cfargs.args and key!='self']
		dc=defaultdict()
		inf=Common.UtilKit.get_cur_info()
		for kv in argpec:
			if kv['value']==None and kv['key'] in inf:
				dc[kv['key']]=inf[kv['key']]
			if kv['value']!=None:
				dc[kv['key']]=kv['value']
		ls=LogStack(**dc)
		ls.insert()
	def WriteErr(self,Message,ClassName=None,MethodName=None,FileLine=None,Leve=3,Result=None,TimeSpans=None,CreatedBy=None,CreatedTime=None):
		self.WriteLog(Message,ClassName,MethodName=MethodName,FileLine=FileLine,Leve=Leve,Result=Result,TimeSpans=TimeSpans,CreatedBy=CreatedBy,CreatedTime=CreatedTime)
	def WriteWar(self,Message,ClassName=None,MethodName=None,FileLine=None,Leve=2,Result=None,TimeSpans=None,CreatedBy=None,CreatedTime=None):
		self.WriteLog(Message,ClassName,MethodName=MethodName,FileLine=FileLine,Leve=Leve,Result=Result,TimeSpans=TimeSpans,CreatedBy=CreatedBy,CreatedTime=CreatedTime)

