import json
import datetime
import inspect
import os
import pdb
class ConstConfig(dict):
	__config__=None
	__BFReadTime__=None
	def __init__(self):
		if not self.__BFReadTime__ or not __config__ or (datetime.datetime.now()-self.__BFReadTime__).total_seconds()>10:
			path=os.path.abspath('{0}\\..\\..\\config.json'.format(inspect.getmodule(self).__file__))
			_config=json.load(open(path,mode='rt'))
			self.__config__=_config
			self.__BFReadTime__=datetime.datetime.now()
			super(ConstConfig,self).__init__(**_config)
		else:
			self.__config__=_config
	def __getattr__(self,key):
		if key in self:
			return self.get(key,None)
		else:
			raise ValueError('Configuration file not exist this attr "%s"!'%key)
	def __setattr__(self,key,value):
		if key in self or key in ('__config__','__BFReadTime__'):
			self[key]=value
		else:
			raise ValueError('Configuration file is read only!'%key)
	def __delattr__(self,key):
		pass
	def __setitem__(self,key,value):
		pass
	def __delitem__(self,key):
		pass