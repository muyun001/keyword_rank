# -*- coding: utf8 -*-
import os
import sys
import json
reload(sys)
sys.setdefaultencoding('utf8')



class SugSogouMobileExtractor(object):

    def extractor(self, body, sug):
        rank = -2
        json_str = body.replace('window.sogou.sug(', '')
        json_str = json_str.replace(')', '')
        data = json.loads(json_str)
        index = 0
        if "s" in data:
            for item in data["s"]:
                index = index + 1
                target = item.lower()
                if sug.lower() in target:
                    rank = index
                    break
        print(rank)
        return rank

if __name__ == '__main__':
    f = open('test/baidu_pc.html', 'r')
    content = f.read()
    f.close()
    ext = SugSogouMobileExtractor()
    ext.extractor(content, '放心投')

