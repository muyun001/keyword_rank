# -*- coding: utf8 -*-
import os
import sys
import traceback

from bs4 import BeautifulSoup
import re
from util.util_getRealAddress import GetReal_Address
import json
from util.domain_urllib import SeoDomain
from base_rank_extractor import BaseRankExtractor

reload(sys)
sys.setdefaultencoding('utf8')

from lxml import etree
from lxml.html import fromstring


class BaiduPCExtractor(BaseRankExtractor):
    def __init__(self):
        super(BaiduPCExtractor, self).__init__()

    def extractor(self, body, ck='', site_name='', pcount=0):
        result = {}

        pos = body.find("</html>")
        if pos < 0 or body.find('location.href.replace') >= 0:
            return 2
        elif body.find('id="wrap"') >= 0 or body.find('<title>') < 0 or body.find('页面不存在_百度搜索') >= 0 \
                or body.find('id="container"') < 0 or body.find('id="content_left"') < 0:
            return 0
        else:
            try:
                tree = fromstring(body)
                ck_domain = self.sx_FindDomain.sxGetDomain(ck)
                containers = tree.cssselect('div.c-container')  # *行代码
                # "c-result result c-clk-recommend"

                result['response_status'] = 1
                if containers:
                    toprank = int(pcount)
                    # result['rank'] = list()  # 只返回一个
                    for container in containers:
                        realaddress = ""
                        domain = ""
                        toprank += 1

                        realaddress_list = container.cssselect("a")
                        if len(realaddress_list) > 0:
                            realaddress = realaddress_list[0].get("href")
                        # domain 显示url
                        domain = self.get_show_url(container)

                        # print domain
                        if ck:
                            # 提供的 url domain > 10 是 显示url 的domain 以 提供url 的domain 开头
                            # 提供的 url domain < 10  完全相等
                            # domain 解析为空 可能是 百度产品

                            if not domain:
                                domain = self.find_realaddress.findReal_Address_improve(realaddress,
                                                                                             domain=domain)  # 真实url
                                if not domain:
                                    continue

                            find_realaddress_state = 0
                            if domain.find("..") > 0:
                                find_realaddress_state = 1
                            domain = self.removeCharacters(self.remove_special_characters(domain))

                            # 显示url
                            show_domain = self.sx_FindDomain.sxGetDomain(domain)[0:15]
                            # if show_domain:
                            #     pass
                            # else:
                            #     # 去除特殊字符 没有 下一个
                            #     continue

                            if str(ck_domain).find(str(show_domain)) > -1:

                                realaddress = self.find_realaddress.findReal_Address_improve(realaddress, domain=domain)  # 真实url
                                realaddress_domain = self.sx_FindDomain.sxGetDomain(self.removeCharacters(realaddress))

                                if ck_domain and realaddress_domain:
                                    if ck_domain == realaddress_domain:
                                        pass
                                    else:
                                        continue
                                else:
                                    continue
                            else:
                                if domain and site_name and site_name != "" and site_name == domain:
                                    pass
                                else:
                                    continue
                        result['domain'] = str(domain).replace("\xc2\xa0", "")
                        result['rank'] = toprank
                        result['realaddress'] = str(realaddress).replace("\xc2\xa0", "")
                        return result
                    return result
                else:
                    return 0
            except Exception:
                print traceback.format_exc()
                return 2
        return result

    def get_show_url(self, container):
        css_list = ['a.c-showurl > span', 'a.c-showurl', 'span.c-showurl', 'div.g', 'span.g']
        domain = ''
        for css in css_list:
            domain_list = container.cssselect(css)
            if len(domain_list) > 0:
                domain = etree.tostring(domain_list[0], encoding="utf-8", method="text").strip()
                if domain != '':
                    break

        return domain

if __name__ == '__main__':
    pass
    b = BaiduPCExtractor()
    # print b.remove_special_characters("www.<b>dhdh</b>")
    f = open('test/baidu_pc.html', 'r')
    content = f.read()
    f.close()
    import time

    start_time = time.time()

    l_s = b.extractor(content, ck='http://www.028twt.cn', site_name='晓晓橙光', pcount=0)

    end_time = time.time()
    print end_time - start_time
    print 'l_s',  l_s
