import logging;logging.basicConfig(level=logging.INFO)
import pymssql
import json
import pdb
import os
from Common.ConfigerManager import ConstConfig
class SqlSerDbHelper():
	def __init__(self,connName='DefaultConnection'):
		self.__connname__=connName
	def create_pool(self):
		cc=ConstConfig()
		_conn=pymssql.connect(**(cc['ConnectionStrings'][self.__connname__]))
		return _conn
	def select(self,sql,**kw):
		logging.info('sql=====>%s',sql)
		logging.info('args=====>%s',json.dumps(kw))
		with self.create_pool() as conn:
			with conn.cursor() as cursor:
				if kw:
					if isinstance(kw,(tuple,list,dict)):
						cursor.execute(sql,kw)
					else:
						raise ValueError("kw 只能是tuple,list,或是dict类型！")
				else:
					cursor.execute(sql)
				return cursor.fetchall()
	def execute(self,sql,**kw):
		logging.info('sql=====>%s',sql)
		logging.info('args=====>%s',json.dumps(kw))
		with self.create_pool() as conn:
			with conn.cursor() as cursor:
				if kw:
					if isinstance(kw,(tuple,list,dict)):
						cursor.execute(sql,kw)
					else:
						raise ValueError("kw 只能是tuple,list,或是dict类型！")
				else:
					cursor.execute(sql)
				return cursor.rowcount

