# -*- coding: utf8 -*-
import sys
from enum import Enum, unique
reload(sys)
sys.setdefaultencoding('utf8')

@unique
class SearchTypeEnums(Enum):
    UrlNotEqual = 1             #不完全相等
    URLAllEqual = 2             #完全相等
    URLDomainCapture = 3        #查排名截图  匹配一级域名
    URLSubDomainCapture = 4     #排名截图  匹配二级域名

