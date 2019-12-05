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
import abc


class BaseRankExtractor(object):
    def __init__(self):
        super(BaseRankExtractor, self).__init__()
        self.find_realaddress = GetReal_Address()
        self.sx_FindDomain = SeoDomain()

    @abc.abstractmethod
    def extractor(self, body, ck='', site_name='', pcount=0):
        return

    def get_real_address_noscript(self, body):
        if body.find("window.location.replace") > 0 and body.find("noscript") > 0:
            start_index = body.find("window.location.replace(")
            cut_body = body[start_index + 25:]
            end_index = cut_body.find("\"")
            cut_url = cut_body[0:end_index]
            return cut_url
        else:
            return None

    # 获取标签下所有中文
    def getText(self, elem):
        rc = []
        for node in elem.itertext():
            rc.append(node.strip())
        return ''.join(rc)

    def removeCharacters(self, previou_url):
        if previou_url.startswith("https://"):
            previou_url = previou_url.replace("https://", "")
        if previou_url.startswith("http://"):
            previou_url = previou_url.replace("http://", "")
        if previou_url.endswith("/"):
            previou_url = previou_url[0:len(previou_url) - 1]
        return previou_url

    def remove_special_characters(self, domain):
        domain = domain.replace("<b>", "")
        domain = domain.replace("</b>", "")
        domain = domain.replace("&nbsp", "")
        domain = domain.replace("....", "")
        domain = domain.replace("...", "")
        return domain

    def removeCharacters(self, previou_url):
        if previou_url.startswith("https://"):
            previou_url = previou_url.replace("https://", "")
        if previou_url.startswith("http://"):
            previou_url = previou_url.replace("http://", "")
        if previou_url.endswith("/"):
            previou_url = previou_url[0:len(previou_url) - 1]
        return previou_url


