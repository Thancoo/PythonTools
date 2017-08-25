import pdb
from Business.Base.BusinessBase import BusinessBase
import json
from collections import defaultdict
import datetime

@CommonDecorator.Injector('UtilKit','CampaignMemberRepository.CampaignMemberRepository','LogHelper.FLLog','ClientHelper.ClientHelper','ConstConfig.ConstConfig')
class CampaignMemberBll(BusinessBase):

    def GetChannelId(self, account, password, brand, campaign):
        return self.campaignmemberRepository.GetChannelId(account, password, brand, campaign)

    def SendBehaviorToAcxiom(self, member):
        sourcename = member.SourceName if not len(
            member.SourceName) > 20 else self.campaignmemberRepository.GetSourceName(member.ChannelId, member.SourceName)
        if not sourcename:
            fLLog.WriteLog(
                'SendBehaviorToAcxiom||memberId:{Id} sourceName is null'.format(member))
        nw = datetime.datetime.now()
        ts = '{:%Y-%m-%d %H:%M:%S.%f}'.format(
            datetime.datetime.now())[0:23][::-1].zfill(23)[::-1]
        sc = defaultdict(credential_type="openId", credentialID=member.OpenId,
                         source_name=sourceName, behavior_code='bhv_LD_004',
                         ts=ts,
                         sign=self.utilKit.md5(self.utilKit.md5(self.constConfig['AppRes']['channelDes%d' % member.ChannelId]+ts).lower()+ts)).lower()
        cc = defaultdict(prize_code='', prize_type='')
        if member.ChannelId == 2:
            cc['prize_name'] = '20元芝华士天猫官方旗舰店优惠券'
        if member.ChannelId == 3:
            if member.GiftType == 4:
                cc['prize_name'] = "8~100元随机微信现金红包"
            elif member.GiftType == 5:
                cc['prize_name'] = "20元芝华士天猫官方旗舰店优惠券"
            elif member.GiftType == 6:
                cc['prize_name'] = "轰趴礼遇"
            else:
                cc['prize_name'] = '20元芝华士天猫官方旗舰店优惠券'
        sc['behavior_content'] = cc
        res = self.clientHelper.Post(
            self.constConfig['AppRes']['Acxiom_Behavior_Url'], json.dump(sc))
        if res['RETURN_CODE'] == '000':
            self.campaignmemberRepository.UpdateSync(member.Id, 2)

    def SendPIIToAcxiom(self, member):
        sourcename = member.SourceName if not len(
            member.SourceName) > 20 else self.campaignmemberRepository.GetSourceName(member.ChannelId, member.SourceName)
        if not sourcename:
            fLLog.WriteLog(
                'SendBehaviorToAcxiom||memberId:{Id} sourceName is null'.format(member))
        nw = datetime.datetime.now()
        ts = '{:%Y-%m-%d %H:%M:%S.%f}'.format(
            datetime.datetime.now())[0:23][::-1].zfill(23)[::-1]
        ax = defaultdict(username=member.NickName, callphone=member.Mobile, openId=member.OpenId,
                         city=member.City, source_name=sourcename, gender='M' if member.Gender == 1 else 'F', ts=ts,
                         sign=self.utilKit.md5(self.utilKit.md5(self.constConfig['AppRes']['channelDes%d' % member.ChannelId]+ts).lower()+ts).lower())
        res = self.clientHelper.Post(
            self.constConfig['AppRes']['Acxiom_PII_Url'], json.dumps(ax))
        if res.RETURN_CODE == '000':
            self.campaignmemberRepository.UpdateSync(member.Id, 1)

