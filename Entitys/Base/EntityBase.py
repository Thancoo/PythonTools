#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
EntityMeta的作用是：
获取和设置值，
"""
import uuid
import logging
logging.basicConfig(level=logging.INFO)
from Entitys.Base.EntityMeta import EntityMeta
from Common.SqlServerDbHelper import SqlSerDbHelper
from collections import defaultdict
from Entitys.Base.ConstParams import QueryPredicate
from Entitys.Base.Field import Field, DateTimeField, StringField, IntField, BooleanField
from Common.ConfigerManager import ConstConfig
import pdb
import datetime

class EntityBase(dict, metaclass=EntityMeta):

    def __init__(self, **kw):
        kw=dict(filter(lambda l:l[0] in self.__mappings__.keys(),kw.items()))
        super(EntityBase, self).__init__(**kw)
        cc = ConstConfig()
        if 'DefaultPageLength' in cc['AppRes']:
            self.__defaultpagelen__ = cc['AppRes']['DefaultPageLength']
            self.__defaultrowcount__ = cc['AppRes']['DefaultRowCount']
        pdb.set_trace()
        if '__TableName__' not in self:
            self['__TableName__']=self.__table__
        pdb.set_trace()

    def __getattr__(self, key):
        try:
            return self[key]
        except KeyError:
            raise AttributeError(
                r"'EntityBase' object has no attribute '%s'" % key)

    def __setattr__(self, key, value):
        self[key] = value

    def getValue(self, key):
        return getattr(self, key, None)

    def getValueOrDefault(self, key, **kw):
        dic = dict(kw if len(kw.keys()) > 0 else self)
        value = dic.get(key, None)
        if value is None:
            field = self.__mappings__[key]
            if not field.not_null:
                return {'key': key, 'value': None}
            if field.default is not None:
                value = (
                    field.default() if callable(field.default) else field.default)
        return {'key': key, 'value': value}

    def next_id(self):
        return '%015d%s000' % (int(time.time() * 1000), uuid.uuid4().hex)

    def find(self, **pk):
        dic = dict(pk if len(pk.keys()) > 0 else self)
        dic = dict(filter(
            lambda _dtk: _dtk[0] in self.__mappings__.keys(), dic.items()))
        sqlhelper = SqlSerDbHelper(self.__ConnStrConfigName__) if hasattr(
            self, '__ConnStrConfigName__') else SqlSerDbHelper()
        #pdb.set_trace()
        sql = '%s WHERE %s' % (self.__select__.format(tableName=self.__TableName__),
                               ' AND '.join([(k+'=%('+k+')'+v.format_symbol[1:])
                                             for k, v in self.__mappings__.items()
                                             if k in dic]) if dic else '1=1')
        if dic.get('Page'):
            if not dic.get('Rows', None):
                dic['Rows'] = self.__defaultrowcount__
            sql = (sql+' Order By '+self.__primary_key__ +
                   ' DESC,[UpdatedOn] DESC OFFSET (%(Page)d-1)*%(Rows)d ROWS FETCH NEXT (Rows)d ROWS ONLY')
        if not dic.get('Available', None):
            dic['Available'] = 1
        rs = sqlhelper.select(
            sql, **dic)
        return (list(map(lambda ix: self.__class__(**ix), rs)) if len(rs) > 0 else None)

    def count(self, **kw):
        dic = dict(kw if len(kw.keys()) > 0 else self)
        dic = dict(
            filter(lambda _dtk: _dtk[0] in self.__mappings__.keys(), dic.items()))
        if not dic.get('Available', None):
            dic['Available'] = 1
        sqlhelper = SqlSerDbHelper(self.__ConnStrConfigName__) if hasattr(
            self, '__ConnStrConfigName__') else SqlSerDbHelper()
        ct = sqlhelper.select('%s WHERE %s' % (self.__count__.format(tableName=self.__TableName__),
                                               ' AND '.join([(k+'=%('+k+')'+v.format_symbol[1:])
                                                             for k, v in self.__mappings__.items()
                                                             if k in dic]) if dic else '1=1'), **dic)
        return (ct[0]['ct'] if len(ct) > 0 else 0)

    def exist(self, **kw):
        dic = dict(kw if len(kw.keys()) > 0 else self)
        dic = dict(
            filter(lambda _dtk: _dtk[0] in self.__mappings__.keys(), dic.items()))
        if not dic.get('Available', None):
            dic['Available'] = 1
        sqlhelper = SqlSerDbHelper(self.__ConnStrConfigName__) if hasattr(
            self, '__ConnStrConfigName__') else SqlSerDbHelper()
        dic['_tableName'] = self.__TableName__
        ct = sqlhelper.select(self.__exist__.format(tableName=self.__TableName, where=' AND '.join([(k+'=%('+k+')'+v.format_symbol[1:])
                                                                                                    for k, v in self.__mappings__.items()
                                                                                                    if k in dic]) if dic else '1=1'), **dic)
        return (len(ct) > 0 and ct[0]['et'] > 0)

    def insert(self, **kw):
        if self.exist():
            raise Exception('not exists specific records')
        args = defaultdict()
        kdv = map(self.getValueOrDefault,
                  filter(lambda px: not self.__mappings__.get(px).is_identity and self.__mappings__.get(px).is_dbfield,
                         self.__fields__))
        kdv = filter(lambda i: i['value'] != None, kdv)
        for itm in kdv:
            args[itm['key']] = itm['value']
        if not self.__mappings__.get(self.__primary_key__).is_identity:
            pk = self.getValueOrDefault(self.__primary_key__)
            args[pk['key']] = pk['value']
        if not args.get('Available', None):
            args['Available'] = 1
        if not args.get('CreatedOn', None):
            args['CreatedOn'] = datetime.datetime.now()
        if not args.get('UpdatedOn', None):
            args['UpdatedOn'] = datetime.datetime.now()
        if not args.get('CreatedBy', None):
            args['CreatedBy'] = 'System'
        if not args.get('UpdatedBy', None):
            args['UpdatedBy'] = 'System'
        sqlhelper = SqlSerDbHelper(self.__ConnStrConfigName__) if hasattr(
            self, "__ConnStrConfigName__") else SqlSerDbHelper()
        #pdb.set_trace()
        rows = sqlhelper.execute(self.__insert__.format(tableName=self.__TableName__, fields=','.join(args.keys()),
                                                        values=','.join([(val.format_symbol[:1]+'('+key+')'+val.format_symbol[-1:])
                                                                         for key, val in self.__mappings__.items()
                                                                         if key in args])), **args)
        return rows > 0

    def update(self, **kw):
        dic = dict(kw if len(kw.keys()) > 0 else self)
        if self.__primary_key__ not in dic:
            raise ValueError('primary key can not be None')
        if not self.exist(**{self.__primary_key__: dic.get(self.__primary_key__)}):
            raise Exception('not exists specific records')
        dic = dict(
            filter(lambda _dtk: _dtk[0] in self.__mappings__.keys(), dic.items()))
        if not dic.get('Available', None):
            dic['Available'] = 1
        if not dic.get('UpdatedBy', None):
            dic['UpdatedBy'] = 'System'
        if not dic.get('UpdatedOn', None):
            dic['UpdatedOn'] = datetime.datetime.now()
        sqlhelper = SqlSerDbHelper(self.__ConnStrConfigName__) if hasattr(
            self, '__ConnStrConfigName__') else SqlSerDbHelper()
        rows = sqlhelper.execute(self.__update__.format(**{'tableName': self.__TableName, 'set': ','.join([(k+'=%'+'('+k+')'+v.format_symbol[1:])
                                                                                                           for k, v in self.__mappings__.items()
                                                                                                           if k in dic and not v.primary_key and v.is_dbfield]),
                                                           self.__primary_key__: '%('+self.__primary_key__+')s'}), **dic)
        return rows > 0

    def delete(self, **kw):
        kw['Available'] = 0
        dic = {'Available': 0, self.__primary_key__: kw.get(
            self.__primary_key__, None)}
        self.update(**kw)
