from Base import EntityBase
from Base.Field import StringFiled,BooleanField,BooleanField,FloatField,IntField
class Publicaccount(EntityBase):
	Id=IntField(primary_key=True)
	Name=StringField(ddl="nvarchar(50)")