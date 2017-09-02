import sys
import pdb
import hashlib
import re
import os
import urllib
import urllib.request
import urllib.parse
import json
import codecs
import chardet
import datetime
from collections import defaultdict

def des_array(arrmt, filter=None):
    ar = []
    for i in arrmt:
        if isinstance(i, list):
            if filter is None:
                ar.extend(i)
            else:
                ar.extend([m for m in i if filter(m)])
        else:
            if filter is None:
                ar.append(i)
            else:
                if filter(i):
                    ar.append(i)
    return ar

def get_cur_info():
    # 前一个frame
    bkf = sys._getframe().f_back
    # 当前frame
    ckf = sys._getframe()
    return {'ClassName': bkf.f_code.co_filename, 'MethodName': bkf.f_code.co_name, 'FileLine': bkf.f_lineno}


def sha512(st):
    sha = hashlib.sha512()
    sha.update(st.encode('ascii'))
    return sha.hexdigest()

def md5(st):
    md5 = hashlib.md5()
    md5.update(st.encode('ascii'))
    return md5.hexdigest()

def timeStamp():
    return round(datetime.datetime.timestamp(datetime.datetime.now()))

def urlEncode(htl):
    return urllib.parse.quote(htl,safe='')

def urlDecode(htl):
    return urllib.parse.unquote(htl)

def convertEncode(path, fromencod, toencode):
    with open(path, mode='r', encoding=fromencod) as fp:
        fc = fp.read()
        lcp = '%s\\cv_%s' % os.path.split(path)
        with open(lcp, mode='w', encoding=toencode) as tp:
            tp.write(fc)


def getTextFromPatt(txt):
    re.compile(
        '(?<="subscribe":false,)("openid":"[\w-^\s]+")(?=,)', re.MULTILINE)
    itr = re.finditer(txt)
    for i in itr:
        yield i


def Get(url, data=None, header=None):
        # url, data=None, headers={}, origin_req_host=None, unverifiable=False,
        # method=None
    pat_query = '^([a-zA-Z0-9-_%]+=[a-zA-Z0-9-_%]+)+(&([a-zA-Z0-9-_%]+=[a-zA-Z0-9-_%]+))?$'
    surl, url, query = None, url, None
    decoderp, allct, res = 'utf8', None, None
    if data and isinstance(data, (dict, list, tuple)):
        query = urllib.parse.urlencode(data)
    elif data and isinstance(data, str):
        if re.search(pat_query, data):
            query = url
        elif re.match('\s*', data):
            pass
        else:
            raise ValueError('query 部分错误:%s' % data)
    if query:
        surl = '{url}?{query}'.format({'url': url, 'query': query})
    else:
        surl = url
    req = None
    if header:
        req = urllib.request.Request(url, headers=header, method='GET')
    else:
        req = urllib.request.Request(url, method='GET')
    with urllib.request.urlopen(req) as rp:
        if rp.status == 200:
            bts = rp.readall()
            if rp.getheader('Content-Type', '').find('charset') > 0:
                decoderp = rp.getheader('Content-Type', '').split('=')[1]
            else:
	            fd = 0
	            ctres = chardet.detect(bts[fd:fd+500])
	            while ctres['confidence'] < 0.9:
	            	fd = (fd+500)
	            	ctres = chardet.detect(bts[fd:fd])
	            decoderp = ctres['encoding']
            allct = str(bts, encoding=decoderp)
            if rp.getheader('Content-Type', '').find('application/json') > 0:
                try:
                    res = json.loads(allct)
                except Exception as e:
                    res = allct
            else:
                res = allct
        else:
            raise Exception("请求出错！")
    return res


def GetTimeFromMultFile(ptpath):
	logevent = [{"TrackingScene": "PageLoad", "TrackingCodeRemark": "安佳淡奶油终极使用指南"},
	{"TrackingScene": "PageLoad", "TrackingCodeRemark": "乳此安佳丨安佳专业乳品专业伙伴"},
	{"TrackingScene": "PageLoad", "TrackingCodeRemark": "变身！小小瑞士卷，玩出新花样"},
	]
	dic = defaultdict()
	dicMap = defaultdict()
	flis = [sf for p, pf, sf in os.walk(ptpath)]
	txtfils = list(['\\'.join([ptpath,fn]) for fn in flis[0] if fn.endswith('.txt')])
	for i in txtfils:
		with open(i) as flcontent:
			dic[os.path.split(i)[1]] = flcontent.read()
	for ftpar in logevent:
		ptn = re.compile(
		    '记录时间：(2017-[0-9]{2}-[0-9]{2} \d{2}:\d{2}:\d{2},[0-9]{1,5})([^\n\r]+[\n\r]{0,2}){4}\n错误描述：[^\r\n]*\"TrackingScene\":\"%(TrackingScene)s\"[^\r\n]*%(TrackingCodeRemark)s[^\n\r]*' % ftpar, re.MULTILINE)
		for k, v in dic.items():
			if ftpar['TrackingCodeRemark'] not in dicMap:
				dicMap[ftpar['TrackingCodeRemark']] = []
			dicMap[ftpar['TrackingCodeRemark']] += [gr.group(1) for gr in ptn.finditer(v)]
	return dicMap
'''
'''
if __name__ == '__main__':
	pathh = 'C:\\Users\\kangyuan\\Desktop\\安佳Tracking数据\\安佳Tracking数据'
	res = GetTimeFromMultFile(pathh)
	with open('\\'.join([pathh, 'res.txt']), 'a') as result:
		result.write('\t'.join(['Title','Time']))
		for title, tirs in res:
			result.write(title)
			for tm in tirs:
				result.write('\t'.join([title,tm]))