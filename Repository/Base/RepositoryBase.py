"""
提供执行Sql的Connection
"""
from Entitys.Base.EntityBase import EntityBase
from Common.SqlServerDbHelper import SqlSerDbHelper
class RepositoryBase():
	__sqlconn__=None
	def __init__(self):
		if not self.__entity__:
			raise ValueError('Response must provit __entity__ argument!')
		if not self.__sqlconn__:
			if self.__entity__.__ConnStrConfigName__:
				self.__sqlconn__=SqlSerDbHelper(self.__entity__.__ConnStrConfigName__)
			else:
				self.__sqlconn__=SqlSerDbHelper()
	def Get(self,entity):
		if isinstance(entity,EntityBase) and isinstance(entity,self.__entity__):
			return entity.find()
		else:
			raise TypeError("entity not instance EntityBase or __entity__")
	def Update(self,entity):
		if isinstance(entity,EntityBase) and isinstance(entity,self.__entity__):
			return entity.update()
		else:
			raise TypeError("entity not instance EntityBase or __entity__")
	def Insert(self,entity):
		if isinstance(entity,EntityBase) and isinstance(entity,self.__entity__):
			return entity.insert()
		else:
			raise TypeError("entity not instance EntityBase or __entity__")
	def Count(self,entity):
		if isinstance(entity,EntityBase) and isinstance(entity,self.__entity__):
			return entity.count()
		else:
			raise TypeError("entity not instance EntityBase or __entity__")
	def Exist(self,entity):
		if isinstance(entity,EntityBase) and isinstance(entity,self.__entity__):
			return entity.exists()
		else:
			raise TypeError("entity not instance EntityBase or __entity__")

