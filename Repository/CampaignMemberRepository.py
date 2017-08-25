from Repository.Base.RepositoryBase import RepositoryBase
from Entitys.CampaignMember import CampaignMember
from Decorator import CommonDecorator
import pandas as pd
import datetime

@CommonDecorator.RepositoryDis(Entity=CampaignMember)
class CampaignMemberRepository(RepositoryBase):

    def GetChannelId(self, account, password, brand, campaign):
        sql = 'SELECT Id FROM PRC_Campaign.dbo.MemberChannel WHERE Account = %(Account)s AND Password = %(Password)s AND Brand = %(Brand)s AND Campaign = %(Campaign)s'
        res = self.__sqlconn__.select(
            sql, Account=account, Password=password, Brand=brand, Campaign=campaign)
        return res[0]['Id'] if res else 0

    def IsSyncByChannelId(self, id):
        sql = 'SELECT  IsSync FROM PRC_Campaign.dbo.MemberChannel WHERE Id = %(Id)d'
        res = self.__sqlconn__.select(sql, Id=id)
        return res and res[0]['IsSync'] == 1

    def GetSourceName(self, channelId, sourceCode):
        sql = 'SELECT SourceName FROM PRC_Campaign.dbo.CampaignSource WHERE ChannelId = %(ChannelId)d AND SourceCode = %(SourceCode)s and Available = 1'
        res = self.__sqlconn__.select(
            sql, ChannelId=channelId, SourceCode=sourceCode)
        return res[0]['sourceName'] if res else ''

    def UpdateSync(self, id, status):
        sql = "UPDATE PRC_Campaign.dbo.CampaignMember SET IsSync = %(IsSync)d,UpdatedOn = %(UpdatedOn)s WHERE Id = %(Id)d"
        res = self.__sqlconn__.execute(
            sql, IsSync=status, Id=id, UpdatedOn=datetime.datetime.now())
        return res
    def AsyncCampaignInfo(self):
        asynclist2=self.Find(CampaignMember(IsSync=2))
        asynclist3=self.Find(CampaignMember(IsSync=3))
        return asynclist2.extend(asynclist3)


