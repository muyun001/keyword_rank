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


class SogouPCExtractor(BaseRankExtractor):
    def __init__(self):
        super(SogouPCExtractor, self).__init__()

    def extractor(self, body, ck='', site_name='', pcount=0):
        """
         获取pc排名数据
         response_status 0请求失败 1 请求成功 2 页面不全，封ip
         360关键词列表页数据
         """
        result = {}
        # 相关搜索
        # result['related'] = []
        # result["rank"] = []
        pos = body.find("</html>")
        if pos < 0:
            return 2
        elif body.find('class="icon_noRes"') >= 0 or body.find(' 抱歉，没有找到与') >= 0:
            return 0
        else:
            ck_domain = ""
            try:
                # print type(tree)
                # 文件提供的url
                if ck:
                    ck_domain = self.sx_FindDomain.sxGetDomain(ck)
                    tree = fromstring(body.decode("utf-8", "ignore"))  # 这种方式 可使用cssselect  不然linux 不能使用
                    result_a = tree.cssselect('div.results>div')
                    if result_a:
                        rank = pcount + 1
                        result['realaddress'] = ck
                        # r['rank'] = -2
                        for each_a in result_a:
                            results = each_a.cssselect('div.fb>a')
                            if not results:
                                results = each_a.cssselect('div>h3>a')

                            if results:
                                # domain_html = etree.tostring(results[0], encoding='utf-8', method='html')
                                # print domain_html
                                domain = results[0].get('href')
                                domain = self.repale_zw(unicode(domain))
                            else:
                                rank += 1
                                continue

                            if domain:
                                # 显示url
                                show_domain = self.sx_FindDomain.sxGetDomain(domain)
                                if show_domain == ck_domain:
                                    # 获取真实 url 的主域， 主域包含 domain 主域ok 代表匹配到

                                    result["rank"] = rank
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

    def repale_zw(self, content):
        list_content = content.split("url=")
        num = len(list_content)
        if num == 2:
            content = urllib.unquote(list_content[1].strip())
        return content

if __name__ == '__main__':
    pass
    b = SogouPCExtractor()
    # print b.remove_special_characters("www.<b>dhdh</b>")
    f = open('test/sogou_pc.html', 'r')
    content = f.read()
    f.close()
    import time

    start_time = time.time()
    # l_s = b.extractor_so_pc_lxml(content, ck="https://www.jianke.com/pfpd/3457258.html", spidertype=4, pcount=0)

    l_s = b.extractor(content, ck='http://www.whcyzx.cnxx', pcount=0)

    # end_time = time.time()
    # print end_time - start_time
    # print b.repale_zw(u"www.tzjob.com/compa... - 1天前")
    print l_s
