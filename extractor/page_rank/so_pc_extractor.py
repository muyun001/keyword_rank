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

reload(sys)
sys.setdefaultencoding('utf8')

from lxml import etree
from lxml.html import fromstring
from base_rank_extractor import BaseRankExtractor


class SoPCExtractor(BaseRankExtractor):
    def __init__(self):
        super(SoPCExtractor, self).__init__()

    def extractor(self, body, ck='', site_name='', pcount=0):

        result = {}
        # 相关搜索
        # result['related'] = []
        # result["rank"] = []
        pos = body.find("</html>")
        if pos < 0:
            return 2
        elif body.find('id="tips"') >= 0 or body.find('抱歉，未找到和 ') >= 0:
            return 0
        else:
            ck_domain = ""
            try:
                # print type(tree)
                # 文件提供的url
                if ck:
                    ck_domain = self.sx_FindDomain.sxGetDomain(ck)
                    tree = fromstring(body.decode("utf-8", "ignore"))  # 这种方式 可使用cssselect  不然linux 不能使用
                    results = tree.cssselect('li.res-list')
                    if results:
                        rank = pcount + 1
                        r = dict()
                        for each in results:
                            domain = ""
                            show_domain = ""
                            if each.cssselect('h3 a'):
                                domain = each.cssselect('h3 a')[0].get("data-url")
                                if not domain:
                                    domain = each.cssselect('h3 a')[0].get("href")
                                    if 'https://www.so.com/link?' in domain:
                                        domain = urllib.unquote(domain.split("url=")[1])
                                        # domain = urllib.unquote(re.findall(r"url=(.*?)", domain)[0])

                            # print domain
                            if domain:
                                # 显示url
                                show_domain = self.sx_FindDomain.sxGetDomain(domain)
                                if ck_domain == show_domain:
                                    # 获取真实 url 的主域， 主域包含 domain 主域ok 代表匹配到
                                    result['realaddress'] = show_domain
                                    result['rank'] = rank
                                    # result["rank"].append(r)
                                    return result
                                else:
                                    rank += 1
                            else:
                                rank += 1
                        return result
                    else:
                        return 0
                else:
                    return 0
            except Exception:
                print traceback.format_exc()
                return 2

if __name__ == '__main__':
    pass
    b = SoPCExtractor()
    # print b.remove_special_characters("www.<b>dhdh</b>")
    f = open('test/so_pc.html', 'r')
    content = f.read()
    f.close()
    import time

    start_time = time.time()
    l_s = b.extractor(content, ck='http://shanghai.gedu.org', pcount=0)

    # end_time = time.time()
    # print end_time - start_time
    print l_s
