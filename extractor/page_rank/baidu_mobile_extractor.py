# -*- coding: utf8 -*-
import os
import sys
import traceback

from bs4 import BeautifulSoup
import re
from util.util_getRealAddress import GetReal_Address
import json
# from util.util_domain import DomainUtil
# from extractor.baidu.sx_domain import FindDomain
from util.domain_urllib import SeoDomain

reload(sys)
sys.setdefaultencoding('utf8')

from lxml import etree
from lxml.html import fromstring
from base_rank_extractor import BaseRankExtractor


class BaiduMobileExtractor(BaseRankExtractor):
    def __init__(self):
        super(BaiduMobileExtractor, self).__init__()

    def extractor(self, body, ck='', site_name='', pcount=0):
        result = {}
        try:
            pos = body.find("</html>")
            if pos < 0:
                return 2
            else:
                tree = fromstring(body)
                containers = tree.cssselect('div.c-result')
                if len(containers) > 0:
                    for container in containers:
                        toprank = ""

                        order = int(container.get('order', 0))
                        if order:
                            toprank = order + int(pcount)

                        if ck:
                            datalog = container.get('data-log', "")
                            if datalog:
                                try:
                                    datalog = str(datalog).replace("\'", "\"")
                                    sx_data = json.loads(datalog)
                                    mu_url = sx_data["mu"]
                                except:
                                    mu_url = ""
                                    continue

                                if mu_url:
                                    mu_urlDomain = self.sx_FindDomain.sxGetDomain(mu_url)
                                    ck_domain = self.sx_FindDomain.sxGetDomain(ck)
                                    if mu_urlDomain != "" and ck_domain != "":
                                        if mu_urlDomain == ck_domain:
                                            pass
                                        else:
                                            continue
                                    else:
                                        continue
                                else:
                                    continue
                            else:
                                continue

                        result['domain'] = ''
                        result['rank'] = toprank
                        if mu_url:
                            result['realaddress'] = mu_url
                        else:
                            result['realaddress'] = ""

                        if ck:
                            return result
                    return result
                else:
                    return 3
        except Exception:
            print traceback.format_exc()
            return -1
        return result

if __name__ == '__main__':
    pass
    b = BaiduMobileExtractor()
    # print b.remove_special_characters("www.<b>dhdh</b>")
    f = open('test/baidu_mobile.html', 'r')
    content = f.read()
    f.close()
    import time

    start_time = time.time()
    l_s = b.extractor(content, ck='http://www.028twt.cn/', site_name='晓晓橙光', pcount=0)
    # l_s = b.extractor(content, ck='http://www.xxx.com/', pcount=0)

    end_time = time.time()
    print end_time - start_time
    print 'l_s',  l_s
