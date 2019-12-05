# -*- coding: utf8 -*-
import sys
from enum import Enum, unique
reload(sys)
sys.setdefaultencoding('utf8')

@unique
class StoreTypeEnums(Enum):
    mysql = 1 #（mysql）
    redis = 2 #（redis）
    elasticsearch = 3 #（elasticsearch）
    mysql_tables = 4 #（mysql分表存储）