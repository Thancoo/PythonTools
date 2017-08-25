"""
所有Controller的继承方法，
Controller用于处理数据，并返回格式化后的Html
获取注入列表并注入！
"""
import os
import inspect
import importlib
import pdb
from collections import defaultdict
from Common.LogHelper import DBLog


class BaseController():
    def __init__(self):
        pass