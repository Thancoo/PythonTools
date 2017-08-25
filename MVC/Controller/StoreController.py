import pdb
from Decorator.HttpDecorator import *
from BaseController import BaseController
from Entitys.Store import Store
from Decorator import CommonDecorator

@CommonDecorator.Injector('StoreBusiness.StoreBusiness')
class StoreController(BaseController):
    @get("/Store/Index")
    def index(self, request):
        store = Store(SalesPersonID=275)
        rcs = self.storeBusiness.Get(store)
        return {'__template__': 'Store/Test.html', "data": {"title": "Hello word!", "content": "Hello Word!", "stores": rcs}}
