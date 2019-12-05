# -*- coding: utf8 -*-
import os
import sys
import json
reload(sys)
sys.setdefaultencoding('utf8')



class Sug360MobileExtractor(object):

    def extractor(self, body, sug):
        rank = -2
        data = json.loads(body)
        index = 0
        if "data" in data:
            data = data['data']
            if 'sug' in data:
                for item in data["sug"]:
                    index = index + 1
                    target = item['word'].lower()
                    if sug.lower() in target:
                        rank = index
                        break
        print(rank)
        return rank

if __name__ == '__main__':
    f = open('test/baidu_pc.html', 'r')
    content = f.read()
    f.close()
    ext = Sug360MobileExtractor()
    ext.extractor(content, '放心投')

