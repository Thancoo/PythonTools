from sys import path
path.append('Base')
path.append('..')
import logging
logging.basicConfig(level=logging.INFO)
from Entitys.Base.EntityBase import EntityBase
from Entitys.Base.Field import Field, StringField, BooleanField, BooleanField, FloatField
import pdb
import time

class User(EntityBase):
    id = StringField(primary_key=True, ddl='varchar(50)')
    email = StringField(ddl='varchar(50)')
    passwd = StringField(ddl='varchar(50)')
    admin = BooleanField()
    name = StringField(ddl='varchar(50)')
    image = StringField(ddl='varchar(500)')
    created_at = FloatField(default=time.time)
