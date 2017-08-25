class QueryPredicate(dict):
	__slots__=('operater','param')
	def __init__(self,operater=None,param=None):
		super(QueryPredicate,self).__init__(operater=operater,param=param)
	def __getattr__(self,key):
		return self.get(key,None)
	def __setattr__(self,key,value):
		if key in self.keys():
			self[key]=value
