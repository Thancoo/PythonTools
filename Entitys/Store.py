#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from sys import path
import logging
logging.basicConfig(level=logging.INFO)
from Entitys.Base.EntityBase import EntityBase
import datetime
from Entitys.Base.Field import Field,StringField,BooleanField,BooleanField,FloatField,IntField,DateTimeField
from Decorator import CommonDecorator
import pdb
import uuid
@CommonDecorator.TableDis(SchemaName='Sales')
class Store(EntityBase):
    BusinessEntityID = IntField(primary_key=True,not_null=True)
    Name = StringField(ddl='varchar(50)',not_null=True)
    SalesPersonID = IntField()
    Demographics = StringField(ddl='varchar(200)',default='')
    rowguid = StringField(ddl='varchar(50)',default=uuid.uuid1,not_null=True)
    ModifiedDate = DateTimeField(default=datetime.datetime.now,not_null=True)