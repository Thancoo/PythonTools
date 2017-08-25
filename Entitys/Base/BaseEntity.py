from Entitys.Base.Field import DateTimeField, StringField, IntField, BooleanField
import datetime

class BaseEntity():
    CreatedOn = DateTimeField(default=datetime.datetime.now())
    CreatedBy = StringField(default='system')
    UpdatedBy = StringField(default='system')
    UpdatedOn = DateTimeField(default=datetime.datetime.now())
    Page = IntField(is_dbfield=False)
    Rows = IntField(is_dbfield=False)
    Available = BooleanField(default=1)
