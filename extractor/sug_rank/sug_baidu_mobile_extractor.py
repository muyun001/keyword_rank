# -*- coding: utf8 -*-
import os
import sys
import json
reload(sys)
sys.setdefaultencoding('utf8')



class SugBaiduMobileExtractor(object):

    def extractor(self, body, sug):
        rank = -2
        if body != "":
            data = json.loads(body)
            index = 0
            if "g" in data:
                for item in data["g"]:
                    index = index + 1
                    target = item['q'].lower()
                    if sug.lower() in target:
                        rank = index
                        break
        print(rank)
        return rank

if __name__ == '__main__':
    f = open('test/baidu_pc.html', 'r')
    content = f.read()
    f.close()
    ext = SugBaiduMobileExtractor()
    ext.extractor(content, '放心投')

