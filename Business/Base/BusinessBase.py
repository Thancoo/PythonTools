import pdb
import sys
from collections import defaultdict
from Common.LogHelper import DBLog
import inspect
import importlib
import os
import logging; logging.basicConfig(level=logging.INFO)


class BusinessBase():
    injectsource = None

    def __init__(self):
        pass
    # 当属性不存在时调用
    def __getattr__(self, key):
        if key in ('Get', 'Update', 'Insert', 'Count', 'Exist') and key in dir(self.__repository__):
            return getattr(self.__repository__, key)
        else:
            raise AttributeError('not exist "{0}" attribute in this object!'.format(key))
