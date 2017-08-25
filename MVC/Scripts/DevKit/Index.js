tts=0;
serverDate=new Date()
$(document).ready(function(){
	configProto();
	//10min请求一次服务器
	//获取时间后，每秒递加一秒
	itv=setInterval(function(){
		serverDate=addSeconds(serverDate,1);
		$('.timestamp-input').val(serverDate.Format('yyyy-MM-dd hh:mm:ss'));
		tts++;
		if(tts>10){
			$.ajax({
				url:"UnixTimeStamp",
				type:"POST",
				success:function(sd){
					tts=0;
					serverDate=new Date(sd.Data*1000);
					$('.timestamp-input').val(serverDate.Format('yyyy-MM-dd hh:mm:ss'));
				},
				error:function(ed){
					//alert(ed);
				}
			});
		}
		//clearInterval(itv);
	},1000);
	$('.sha512click').click(function(){
		$.ajax({
			url:"Sha512Hash",
			type:"POST",
			data:$('.sha512-input').val(),
			success:function(sd){
				$('.sha512-result').val(sd.Data);
			},
			error:function(ed){
				alert(ed);
			},
		});
	});
	$('.md5click').click(function(){
		$.ajax({
			url:"Md5Hash",
			type:"POST",
			data:$('.MD5-input').val(),
			success:function(sd){
				$('.MD5-result').val(sd.Data);
			},
			error:function(ed){
				alert(ed);
			},
		});
	});
	$('.refreshtimestamp').click(function(){
		$.ajax({
			url:"UnixTimeStamp",
			type:"POST",
			success:function(sd){
				serverDate=new Date(sd.Data*1000);
				tts=0;
				$('.timestamp-input').val(serverDate.Format('yyyy-MM-dd hh:mm:ss'));
				$('.remanberst').val(sd.Data);
			},
			error:function(ed){
				alert(ed);
			},
		});
	});
	$('.urlencodeclick').click(function(){
		if($('.urlencode-input').val().length<1){
			alert('Raw Url 不可为空！');
		}
		reqdata={"Option":$(this).data("option"),"Url":$('.urlencode-input').val()};
		$.ajax({
			url:"UrlEncode",
			type:"POST",
			data:JSON.stringify(reqdata),
			success:function(sd){
				if(sd.State){
					$('.urlencode-result').val(sd.Data);
				}else{
					alert(sd.Data)
				}
			},
			error:function(ed){
				alert(ed.Message);
			},
		});
	});
	$('.dynamicParamList').on('click','.extparam-input-remove',function(){
		if($('.dynamicParamList>.extparam').length==1){
          	$('.dynamicParamList>.extparam').first().find('input').val('');
          	return;
		}
		$(this).parents('.extparam').first().remove()
	});
	$('.addparam').click(function(){
		htbd='<div class="extparam">\
            <div class="name"><input class="form-control extparam-input-name" id="Host" placeholder="name" type="text"></div>\
            <div class="value fullwight"><input class="form-control extparam-input-value" id="Host" placeholder="value" type="text"></div>\
            <div class="option"><button class="glyphicon glyphicon-remove form-control extparam-input-remove"></button></div>\
          </div>';
          $('.dynamicParamList>.extparam').last().after($(htbd));
	});
	$('.lexertemplate').click(function(){
		if($('.template').val().length<1){
			alert('Template必须填写！');
		};
		postdata={"Template":$('.template').val()};
		if($('.dynamicParamList>.extparam').first().find('.extparam-input-name').val().length>0 || $('.dynamicParamList>extparam').length>0){
			postdata["ExtParam"]={};
			for(itm in $('.dynamicParamList>.extparam')){
				postdata["ExtParam"][$('.dynamicParamList>.extparam').eq(itm).find('.extparam-input-name').val()]=$('.dynamicParamList>.extparam').eq(itm).find('.extparam-input-value').val();
			}
		}
		$.ajax({
			url:"LexersTemplate",
			type:"POST",
			data:JSON.stringify(postdata),
			success:function(sd){
				if(sd.State)
					$('.templateresult').val(sd.Data);
				else
					alert(sd.Message)
			},
			error:function(ed){
				alert(ed);
			},
		});
	});
});
function addSeconds(date,sg){
	if(!date instanceof Date)
		return null;
	return new Date(date.getTime()+sg*1000);
}
function configProto(){
	Date.prototype.Format = function(fmt)
	{ 
		var o = {
			"M+" : this.getMonth()+1,                 //月份
			"d+" : this.getDate(),                    //日
			"h+" : this.getHours(),                   //小时
			"m+" : this.getMinutes(),                 //分
			"s+" : this.getSeconds(),                 //秒
			"q+" : Math.floor((this.getMonth()+3)/3), //季度
			"S"  : this.getMilliseconds()             //毫秒
		};
		if(/(y+)/.test(fmt))
			fmt=fmt.replace(RegExp.$1, (this.getFullYear()+"").substr(4 - RegExp.$1.length));
		for(var k in o)
			if(new RegExp("("+ k +")").test(fmt))
		fmt = fmt.replace(RegExp.$1, (RegExp.$1.length==1) ? (o[k]) : (("00"+ o[k]).substr((""+ o[k]).length)));   
		return fmt;
	}
}