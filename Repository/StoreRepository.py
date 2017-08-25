import pdb
import logging;logging.basicConfig(level=logging.INFO)
from Decorator import CommonDecorator
from Repository.Base.RepositoryBase import RepositoryBase
from Entitys.Store import Store
@CommonDecorator.RepositoryDis(Entity=Store)
class StoreRepository(RepositoryBase):
	logging.info('StoreRepository实例化完成')
	pass
