# -*- coding: utf8 -*-
import sys
from enum import Enum, unique
reload(sys)
sys.setdefaultencoding('utf8')

@unique
class DeviceEnums(Enum):
    baidu_pc = 1
    baidu_mobile = 2
    pc_360 = 3
    sogou_pc = 4
    sm_mobile = 5
    sug_baidu_pc = 6
    sug_baidu_mobile = 7
    sug_360_pc = 8
    sug_360_mobile = 9
    sug_sogou_pc = 10
    sug_sogou_mobile = 11
    sug_sm_mobile = 12