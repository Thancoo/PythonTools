from Entitys.Base.Field import StringField, IntField, BooleanField
from Entitys.Base.EntityBase import EntityBase
from Entitys.Base.BaseEntity import BaseEntity
from Decorator.CommonDecorator import TableDis


@TableDis(ConnStrConfigName='141Connection', DbName='PRC_Campaign', SchemaName='dbo')
class CampaignMember(BaseEntity, EntityBase):
    Id = IntField(primary_key=True, not_null=True)
    OpenId = StringField()
    Mobile = StringField()
    Gender = StringField()
    City = StringField()
    Province = StringField()
    Country = StringField()
    ChannelId = IntField()
    Birthday = StringField()
    AppId = StringField()
    Status = IntField()
    NickName = StringField()
    Email = StringField()
    IsGift = BooleanField()
    GiftType = IntField()
    GiftName = StringField()
    GiftDate = StringField()
    GiftWay = StringField()
    ExchangeCode = StringField()
    IsUsed = BooleanField()
    UsedDate = StringField()
    IsSync = BooleanField()
    SourceName = StringField()
