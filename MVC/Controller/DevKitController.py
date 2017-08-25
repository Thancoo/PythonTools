#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import pdb
import asyncio
from Decorator import CommonDecorator
from Decorator.HttpDecorator import *
from BaseController import BaseController
import jinja2
import json

@CommonDecorator.Injector('UtilKit')
class DevKit(BaseController):
    @get("/DevKit/Index")
    def index(self, request):
        return {'__template__': 'DevKit/Index.html'}

    @post("/DevKit/Sha512Hash")
    async def Sha512Hash(self, request):
        dt_txt = await request.text()
        if dt_txt and len(dt_txt)<1:
            return {'State':False,'Data':'请求内容不可为空！'}
        req = self.utilKit.sha512(dt_txt)
        return {'State': True, 'Data': req}

    @post("/DevKit/Md5Hash")
    async def Md5Hash(self, request):
        dt_txt = await request.text()
        if dt_txt and len(dt_txt)<1:
            return {'State':False,'Data':'请求内容不可为空！'}
        req = self.utilKit.md5(dt_txt)
        return {'State': True, 'Data': req,'Message':'请求成功！'}

    @post("/DevKit/UrlEncode")
    async def UrlEncode(self, request):
        dt_txt = await request.text()
        req_json=json.loads(dt_txt)
        if dt_txt and len(dt_txt)<1:
            return {'State':False,'Data':'请求内容不可为空！'}
        if 'Option' not in req_json:
            return {'State': False, 'Data': "Option不可为空！",'Message':'Option不可为空！'}
        if req_json['Option'] not in ['encodeurl','decodeurl']:
            return {'State': False, 'Data': "Option值只可为encodeurl或decodeurl！",'Message':'Option值只可为encodeurl或decodeurl！'}
        if 'Url' not in req_json:
            return {'State': False, 'Data': "Url不可为空！",'Message':'Url不可为空！'}
        try:
            if req_json['Option']=='encodeurl':
                req = self.utilKit.urlEncode(req_json['Url'])
            else:
                req = self.utilKit.urlDecode(req_json['Url'])
            return {'State': True, 'Data': req,'Message':'请求成功！'}
        except Exception as ex:
            return {'State': False, 'Data': ex,'Message':ex.__str__()}

    @post("/DevKit/UnixTimeStamp")
    def UnixTimeStamp(self, request):
        req = self.utilKit.timeStamp()
        return {'State': True, 'Data': round(req)}
    @post('/DevKit/LexersTemplate')
    async def LexersTemplate(self,request):
        req_txt=await request.text()
        req_json=json.loads(req_txt)
        if 'Template' not in req_json:
            return {'State': False, 'Data': None,'Message':'Template不可为空！'}
        jinja2.clear_caches()
        temp=jinja2.Template(req_json['Template'])
        temp.globals['sha512']=self.utilKit.sha512
        temp.globals['md5']=self.utilKit.md5
        temp.globals['timeStamp']=self.utilKit.timeStamp
        temp.globals['urlEncode']=self.utilKit.urlEncode
        temp.globals['urlDecode']=self.utilKit.urlDecode
        if 'ExtParam' in req_json and isinstance(req_json['ExtParam'],dict):
            for key,value in req_json['ExtParam'].items():
                temp.globals[key]=value
        try:
            return {'State': True, 'Data': temp.render(),'Message':"请求成功！"}
        except Exception as ex:
            return {'State': False, 'Data': ex,'Message':ex.__str__()}

