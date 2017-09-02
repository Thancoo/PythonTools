import logging; logging.basicConfig(level=logging.INFO)
import json
import functools
import inspect
import os
import copy
from collections import defaultdict
from Common.ConfigerManager import ConstConfig
import Common.UtilKit
import pdb
import importlib
import re
"""
为了实现懒加载，在这里只是把要注入的函数列表放到cls里，
decorator与Mate，父类init的执行顺序如下
Mate
decorator
init
注意：这里的注入列表的第一个，有特殊意义：
代表这个Buiness所对应的Repository，
并为Buiness提供基础的增删改查功能。
"""
# 注入类型列表：静态资源
__injectsource__ = None

def Injector(*args):
    def decorator(cls):
        global __injectsource__
        logging.info('%s=======注入列表=====》%s', cls.__name__, json.dumps(args))
        cls.__injector__ = args
        if not __injectsource__:
            dic = defaultdict()
            path = os.path.abspath(inspect.getmodule(Injector).__file__)
            root = os.path.abspath('{0}\\..\\'.format(os.path.split(path)[0]))
            try:
                constConfig=ConstConfig()
                ijconfig=constConfig['InjectorConfig']['InjectorRootPath']
                for k,v in ijconfig.items():
                    dic[k]=dict(tp='package', path="{0}\\{1}".format(root,v))
            except Exception as e:
                raise e
            for pkname, pkdt in dic.items():
                pkdt['modules']=defaultdict()
                for pfn, sfn, sfs in os.walk(pkdt['path']):
                    if pfn.partition(pkname)[2] and not re.fullmatch('[a-zA-Z\\\\]+',pfn.partition(pkname)[2]):
                        continue
                    for pdp in sfs:
                        if not pdp.endswith(".py") or pdp.startswith("__") or pdp.endswith("Base.py"):
                            continue
                        ptp="{0}.{1}".format('.'.join(pfn.partition(pkname)[1:]).replace('\\','.'), pdp[0:-3])
                        ptp=ptp.replace('..','.')
                        if ptp.endswith('.'):
                            ptp=ptp[0:-1]
                        pkdt['modules'][pdp[0:-3]]={"tp": "module", "path": ptp}
            __injectsource__ = copy.deepcopy(dic)
        ii = [i.lower() for i in cls.__injector__]
        for pkgn, pkge in __injectsource__.items():
            for modn, mode in pkge['modules'].items():
                for ij in ii:
                    if mode['tp']=='module' and ij.startswith(modn.lower()):
                        im=importlib.import_module(mode['path'])
                        if im:
                            if ij.find('.')>-1:
                                pdb.set_trace()
                                for mb in dir(im):
                                    if not re.fullmatch('[a-zA-Z][a-zA-Z0-9_]+',mb):
                                        continue
                                    pdb.set_trace()
                                    if ij.endswith(mb.lower()) and inspect.isclass(getattr(im,mb)):
                                        pdb.set_trace()
                                        _clsna=''.join([mb[0].lower(),mb[1:]])
                                        setattr(cls, _clsna,getattr(im,mb)())
                            else:
                                _modn=''.join([modn[0].lower(),modn[1:]])
                                setattr(cls, _modn,im)
                        else:
                            pdb.set_trace()
                            raise('Module查找出错')
        return cls
    return decorator

'''
TableDis主要功能是为Entity加入额外的数据：
链接字符串
数据库名称
架构名称
表名称
！如果未提供，则赋予默认值！
'''
def TableDis(ConnStrConfigName='DefaultConnection', DbName=None, SchemaName='dbo', TableName=None):
    def decorator(tp):
        config = ConstConfig()
        tp.__ConnStrConfigName__ = ConnStrConfigName
        tp.__DbName__ = DbName
        tp.__SchemaName__ = SchemaName
        if not DbName:
            con = config['ConnectionStrings'][ConnStrConfigName]
            stcon = (con['database'] if ConnStrConfigName !=
                     'MySqlConnection' else con['DefaultDb'])
            tp.__DbName__ = stcon
        if TableName:
            tp.__TableName__ = '{0}.{1}.{2}'.format(
                tp.__DbName__, tp.__SchemaName__, TableName)
        else:
            tp.__TableName__ = '{0}.{1}.{2}'.format(
                tp.__DbName__, tp.__SchemaName__, tp.__name__)
        # logging.info('%s=========设置Table=====》%s',tp.__name__,tp.__TableName__)
        return tp
    return decorator
def RepositoryDis(Entity=None):
    def decorator(tp):
        # logging.info('%s======设置Rep=======>%s',tp.__name__,Entity.__name__)
        tp.__entity__=Entity
        return tp
    return decorator
