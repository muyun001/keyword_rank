# -*- coding: utf8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf8')
import urllib


class DomainUtil(object):

    @staticmethod
    def format_validate(domain):
        pass

    @staticmethod
    def get_domian(url):
        if not url.startswith('http'):
            url = 'http://'+url
        proto, rest = urllib.splittype(url)
        res, rest = urllib.splithost(rest)
        return None if not res else res

    def sxGetDomain(self, url):
        if not url.startswith('http'):
            url = 'http://'+url
        proto, rest = urllib.splittype(url)
        res, rest = urllib.splithost(rest)
        print res, rest
        return None if not res else res

if __name__ == '__main__':
    d = DomainUtil()
    # print d.get_domian('m.bioderma.net.cn')
    print d.sxGetDomain('https://m.baidu.com/from=844b/s?pn=10&usm=9&word=%E6%8B%9B%E8%81%98&sa=np&rsv_pq=13244013869038379036&rsv_t=a57cheu0zg5NWSDEwvYEoCXW%252FDQAHw4mb5xiQTqmKnL7Iz%252FN0RHuNBedeQ&ant_ct=sLRbCCquN83UA64DHkWhkEDXvfIHnNhzT1SvYCG%2FSzNOfTnVqUvaLvfxu0BAs3b%2F&ms=1&rqid=13244013869038379036&adid=b7cc3071b061201c&tj=1')
