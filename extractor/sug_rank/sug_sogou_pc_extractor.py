# -*- coding: utf8 -*-
import os
import sys
import json
reload(sys)
sys.setdefaultencoding('utf8')



class SugSogouPCExtractor(object):

    def extractor(self, body, sug):
        rank = -2
        json_str = body.replace('window.sogou.sug(', '')
        json_str = json_str.replace(',-1);', '')
        data = json.loads(json_str)
        index = 0
        if len(data) >1 and isinstance(data[1], list):
            for item in data[1]:
                index = index + 1
                target = item.lower()
                if sug.lower() in target:
                    rank = index
                    break
        print(rank)
        return rank

if __name__ == '__main__':
    # f = open('test/baidu_pc.html', 'r')
    # content = f.read()
    # f.close()
    # ext = SugSogouPCExtractor()
    # ext.extractor(content, '放心投')
    str = '["texdrwerqwe23qwerwst",["新浪","新商盟","修罗武神"],["0;10;0;0","1;10;0;0","2;10;0;0"],["","",""],["0"],"","suglabId_1"]'
    data = json.loads(str)
    print(len(data))
    print(isinstance(data[1], list))

