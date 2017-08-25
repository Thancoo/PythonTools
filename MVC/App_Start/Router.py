from sys import path
import os
from collections import defaultdict
import re
import logging
logging.basicConfig(level=logging.INFO)
import pdb
import importlib
import inspect
from Common import UtilKit
from BaseController import BaseController
"""
router的作用是，返回所有
Controller名称，Action名称，
(动态参数如何，只能一次注册么)
"""


class Router():

    def add_route(self, app, fn):
        method = getattr(fn, '__method__', None)
        path = getattr(fn, '__route__', None)
        if path is None or method is None:
            raise ValueError('@get or @post not defined in %s.' % str(fn))
        if not asyncio.iscoroutinefunction(fn) and not inspect.isgeneratorfunction(fn):
            fn = asyncio.coroutine(fn)
        logging.info('add route %s %s => %s(%s)' % (
            method, path, fn.__name__, ', '.join(inspect.signature(fn).parameters.keys())))
        app.router.add_route(method, path, RequestHandler(app, fn))
    '''
    根据包注入
    （需要将要注入的目录放到Sys.Path中）
    遍历目录，找出所有Module，过滤掉不是Controller.py结尾的Module。
    实例化Module中的Controller
    获取Controller中的方法作为Action
    '''
    def add_routes(self, app, module_name):
        logging.info('开始加载Router')
        n = module_name.find('.')
        if n == (-1):
            mifo = importlib.machinery.PathFinder.find_module(module_name)
            _tpmod = mifo.load_module()
        else:
            mifo = importlib.find_module(module_name[n:])
            _tpmod = mifo.load_module()
        # 找出继承自ControllerBase的类。
        # 文件必须以Controller结尾。
        controllerDir = os.path.abspath(_tpmod.__file__) if not os.path.isfile(
            os.path.abspath(_tpmod.__file__)) else os.path.dirname(os.path.abspath(_tpmod.__file__))
        controllers = [sf for p, sd, sf in os.walk(controllerDir)]
        filter = lambda x: not isinstance(
            x, list) and x != 'BaseController.py' and x.endswith("Controller.py")
        while len([p for p in controllers if isinstance(p, list)]) > 0:
            controllers = UtilKit.des_array(controllers, filter)
        controllers = map(lambda o: o[0:-3], controllers)
        logging.info(controllers)
        for cm in controllers:
            logging.info("开始加载Module：%s" % cm)
            _mdp = importlib.machinery.PathFinder.find_module(cm)
            if not _mdp:
                raise Exception("该Module不存在或不在工作目录！")
            md = _mdp.load_module()
            for cl in dir(md):
                _ctr = getattr(md, cl, None)
                if inspect.isclass(_ctr) and BaseController in _ctr.__bases__:
                    ctr = _ctr()
                    logging.info('发现Controller：%s' % cl)
                    for ac in dir(ctr):
                        oac = getattr(ctr, ac, None)
                        method = getattr(oac, '__method__', None)
                        path = getattr(oac, '__route__', None)
                        if method and path:
                            logging.info('记录action：%s' % oac.__name__)
                            logging.info('path:%s' % path)
                            app.router.add_route(method, path, oac)
