#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import pdb
from sys import path
import logging; logging.basicConfig(level=logging.INFO)
import copy
from Common.ConfigerManager import ConstConfig
from Entitys.Base.Field import Field,StringField,BooleanField,BooleanField,FloatField,IntField,DateTimeField

class EntityMeta(type):
    def __new__(cls, name, bases, attrs):
        # 排除Model类本身:
        if name=='EntityBase':
            return type.__new__(cls, name, bases, attrs)
        # 获取所有的Field，包括父类继承的Item:
        _attrs=copy.deepcopy(attrs)
        for clt in bases:
            for f in dir(clt):
                if isinstance(getattr(clt,f),Field) and f not in _attrs:
                    _attrs[f]=getattr(clt,f)
        tableName = attrs.get('__table__', None) or name
        #logging.info('found model: %s (table: %s)' % (name, tableName))
        # 获取所有的Field和主键名:
        mappings = dict()
        fields = []
        primaryKey = None
        for k, v in _attrs.items():
            if isinstance(v, Field) and v.is_dbfield:
                mappings[k] = v
                if v.primary_key:
                    # 找到主键:
                    if primaryKey:
                        raise RuntimeError('Duplicate primary key for field: %s' % k)
                    primaryKey = k
                else:
                    fields.append(k)
        if not primaryKey:
            raise RuntimeError('Primary key not found.')
        for k in mappings.keys():
            _attrs.pop(k)
        _attrs['__mappings__'] = mappings # 保存属性和列的映射关系
        _attrs['__table__'] = tableName
        _attrs['__primary_key__'] = primaryKey # 主键属性名
        _attrs['__fields__'] = fields # 除主键外的属性名
        # 构造默认的SELECT, INSERT, UPDATE和DELETE语句:
        _attrs['__select__'] = 'SELECT %s, %s FROM %s' % (primaryKey, ', '.join(mappings.keys()), '{tableName}')
        _attrs['__insert__'] = 'INSERT INTO %s (%s) VALUES (%s)' % ('{tableName}','{fields}','{values}')#', '.join(filter(lambda k:not mappings[k].is_identity,mappings.keys())),', '.join([(val.format_symbol[:1]+'('+key+')'+val.format_symbol[-1:]) for key,val in mappings.items() if not val.is_identity]))
        _attrs['__update__'] = 'UPDATE %s SET %s WHERE %s=%s' % ('{tableName}','{set}',primaryKey,'%({0})s'.format(primaryKey))#set with primaryKey需要替换
        _attrs['__delete__'] = 'DELETE FROM %s WHERE %s=%s' % ('{tableName}', primaryKey,'%({0})s'.format(primaryKey))#primaryKey 需要替换
        _attrs['__count__']='SELECT COUNT(%s) ct FROM %s'%(primaryKey,'{tableName}')
        _attrs['__exist__']='SELECT 1 et WHERE EXISTS(SELECT 1 FROM %s WHERE %s)'%('{tableName}','{where}')
        return type.__new__(cls, name, bases, _attrs)