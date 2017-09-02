from Entitys.Base.EntityBase import EntityBase
from Entitys.Base.Field import IntField,StringField,FloatField
from Entitys.Base.BaseEntity import BaseEntity
from Decorator import CommonDecorator
import datetime
@CommonDecorator.TableDis()
class LogStack(BaseEntity,EntityBase):
	Id=IntField(primary_key=True,is_identity=True,not_null=True)# BIGINT NOT NULL IDENTITY(1,1),
	ProjectName=StringField(ddl='NVARCHAR(200)',default='SyncDataTools')#NVARCHAR(200),
	ClassName=StringField(ddl='NVARCHAR(200)',default='')# NVARCHAR(200),
	MethodName=StringField(ddl='NVARCHAR(200)',default='')# NVARCHAR(200),
	FileLine=IntField(default=0)# INT,
	Leve=IntField(default=1)# INT,
	Message=StringField(ddl='NVARCHAR(500)',default='')# NVARCHAR(500),
	Result=StringField(ddl='NVARCHAR(1000)',default='')# NVARCHAR(1000),
	TimeSpans=FloatField(default=0.0)# DECIMAL,