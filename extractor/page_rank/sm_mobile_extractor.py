# -*- coding: utf8 -*-
import os
import sys
import traceback
import urllib
from bs4 import BeautifulSoup
import re
from util.util_getRealAddress import GetReal_Address
import json
# from util.util_domain import DomainUtil
# from extractor.baidu.sx_domain import FindDomain
from util.domain_urllib import SeoDomain
from lxml import html

reload(sys)
sys.setdefaultencoding('utf8')

from lxml import etree
from lxml.html import fromstring
from base_rank_extractor import BaseRankExtractor


class SmMobileExtractor(BaseRankExtractor):
    def __init__(self):
        super(SmMobileExtractor, self).__init__()

    def extractor(self, body, ck='', site_name='', pcount=0):
        result = {}
        # 相关搜索
        # result['related'] = []
        # result["rank"] = []
        pos = body.find("</html>")
        if pos < 0:
            return 2
        elif body.find('id="no-result-info card"') >= 0 or body.find('抱歉，没有找到') >= 0:
            return 0
        else:
            try:
                if ck:
                    ck_domain = self.sx_FindDomain.sxGetDomain(ck)
                    tree = fromstring(body.decode("utf-8", "ignore"))  # 这种方式 可使用cssselect  不然linux 不能使用
                    results = tree.cssselect('div#results>div')
                    if results:
                        rank = pcount + 1
                        num = 0
                        for i, n in enumerate(results):
                            ad_alert = n.cssselect('div.ad-alert-info')
                            if ad_alert:
                                num = i
                        result['realaddress'] = ck
                        # r['rank'] = -2
                        for v, res in enumerate(results):
                            # if v > num:
                            ad_url = res.get('ad_dot_url')
                            if ad_url:
                                continue
                            else:
                                hide = res.cssselect('div.sc-show-hide-wrap')
                                if hide:
                                    res = hide[0].xpath('./div')
                                    domain = list()
                                    for each_res in res:
                                        domain.append(self.domain_url(each_res))
                                else:
                                    domain = [self.domain_url(res)]
                                if domain:
                                    for each in domain:
                                        if each == '':
                                            rank += 1
                                            continue
                                        link = each.get('href')
                                        if not link:
                                            continue

                                        if "javascript:;" in link:
                                            rank += 1
                                            continue

                                        show_domain = self.sx_FindDomain.sxGetDomain(link)
                                        show_link = each.get('data-recoorgi')
                                        show_link = show_link if show_link else ""
                                        show_url = self.sx_FindDomain.sxGetDomain(show_link)


                                        # print show_domain
                                        if show_domain == ck_domain or show_url == ck_domain:
                                            # 获取真实 url 的主域， 主域包含 domain 主域ok 代表匹配到
                                            result['domain'] = show_domain
                                            result['rank'] = rank
                                            return result
                                        else:
                                            rank += 1
                                else:
                                    rank += 1
                                    continue
                        return result
                    else:
                        return 0
                else:
                    return 0
            except Exception:
                print traceback.format_exc()
                # print etree.tostring(each, encoding='utf-8', method='html')
                return 2

    def domain_url(self, res):
        domain = res.xpath('./h2/a')
        if not domain:
            # domain = res.xpath('./a[1]')
            domain = res.cssselect("a")
            if not domain:
                domain = res.cssselect('a.c-header-inner')
                if not domain:
                    domain = res.cssselect('div.c-container>a.c-nature--v1_0_0')
                    if not domain:
                        domain = res.cssselect('a.wemedia_header')
        if len(domain) > 1:
            domain = domain[0]
        else:
            if not domain:
                domain = ''
            else:
                domain = domain[0]
        return domain

if __name__ == '__main__':
    pass
    b = SmMobileExtractor()
    # print b.remove_special_characters("www.<b>dhdh</b>")
    f = open('test/sm_mobile.html', 'r')
    content = f.read()
    f.close()
    import time

    start_time = time.time()
    l_s = b.extractor(content, ck='www.yishengfeng.cn', pcount=0)

    # end_time = time.time()
    # print end_time - start_time
    # print b.repale_zw(u"www.tzjob.com/compa... - 1天前")
    print l_s
