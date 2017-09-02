from BaseController import BaseController
from Decorator import CommonDecorator
from Decorator import HttpDecorator

@CommonDecorator.Injector('CampaignMemberBusiness.CampaignMemberBusiness')
class CampaignMemberController(BaseController):
	@HttpDecorator.get('/CampaignMember/Index')
	def Index(self, request):
	    id = self.campaignmemberBusiness.Get(CampaignMember(OpenId='o3vWouLoDpDpLAyUegeF4E2uT_80'))
	    return {'__template__':'CampaignMember/Index.html',\
	    			"data":{\
	    				"title":"Hello word!",\
	    				"content":"Hello Word!",\
	    				"id":id\
	    			}
	    		}