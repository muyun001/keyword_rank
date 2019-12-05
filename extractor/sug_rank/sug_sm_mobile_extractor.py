# -*- coding: utf8 -*-
import os
import sys
import json
reload(sys)
sys.setdefaultencoding('utf8')



class SugSmMobileExtractor(object):

    def extractor(self, body, sug):
        rank = -2
        data = json.loads(body)
        index = 0
        if "r" in data:
            for item in data["r"]:
                index = index + 1
                target = item["w"].lower()
                if sug.lower() in target:
                    rank = index
                    break
        print(rank)
        return rank

if __name__ == '__main__':
    f = open('test/baidu_pc.html', 'r')
    content = f.read()
    f.close()
    ext = SugSmMobileExtractor()
    ext.extractor(content, '放心投')

