import urllib.request
import urllib.parse
import urllib.error
import json
import re
pat_query = '^\?([a-zA-Z0-9-_%]+=[a-zA-Z0-9-_%]+)+(&([a-zA-Z0-9-_%]+=[a-zA-Z0-9-_%]+))?$'
pat_url = ''
pat_header_charset = 'charset[ ]*=[ ]*([^\s]+)'


class ClientHelper():

    def Get(self, url, data=None, header=None):
            # url, data=None, headers={}, origin_req_host=None, unverifiable=False, method=None
                # url, data=None, headers={}, origin_req_host=None, unverifiable=False,
        # method=None
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
            pdb.set_trace()
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
        return res

    def Post(self, url, data, headers=None):
        # url, data=None, headers={}, origin_req_host=None, unverifiable=False,
        # method=None
        res = None
        encoderp = 'utf-8'
        allct = None
        contenttype = ''
        if not header:
            header = dict()
        if 'content-type' in map(lambda x: x.lower(), header.keys()):
            header['Content-Type'] = 'application/json'
        dtbs = (data if isinstance(data, basestring)
                else json.dumps(data)).encode('utf8')
        header['content-length'] = len(dtbs)
        req = urllib.request.Request(
            url, data=dtbs, headers=headers, method='POST')
        with urllib.request.urlopen(req) as rp:
            if rp.status == 200:
                allbts = rp.readall()
                if rp.getheader('Content-Type', '').find('charset') > 0:
                    decoderp = rp.getheader('Content-Type', '').split('=')[1]
                else:
                    fd = 0
                    ctres = chardet.detect(allbts[fd:fd+500])
                    while ctres['confidence'] < 0.9:
                        fd = (fd+500)
                        ctres = chardet.detect(allbts[fd:fd])
                    decoderp = ctres['encoding']
                allct = str(allbts, encoding=decoderp)
                if rp.getheader('Content-Type', '').find('application/json') > 0:
                    try:
                        res = json.loads(allct)
                    except Exception as e:
                        res = allct
                else:
                    res = allct
        return res
