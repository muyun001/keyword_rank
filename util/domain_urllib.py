# -*- coding: utf8 -*-

# import urlparse
import re
from postfix_config import postfix_list


class SeoDomain(object):
    def __init__(self):
        pass

    def _get_postfix(self, domain):
        res = domain
        if domain in postfix_list or '.' + domain in postfix_list:
            return 'error'
        pattern = r'[^\.]+(' + '|'.join([h.replace('.', r'\.') for h in postfix_list]) + ')$'
        result = re.findall(pattern, domain)
        if result:
            r = result[0]
            arr = r.split('.')
            if len(arr) == 2 and len(domain.split('.')) > 2:
                if '.' + domain.split('.')[-2] in postfix_list:
                    return '.' + domain.split('.')[-2] + '.' + arr[1]
            return result[0]
        else:
            return None

    def get_second_domain(self, url):
        url = self.removeCharacters(url)
        if url.find("/") > -1:
            url = url[0: url.rindex("/")]
        if not url:
            return None
        res = self._clear_info(url)
        return res if res else ""

    def _clear_info(cls, domain):
        res = re.sub(r'(?:(http://|https://|ftps://))', '', domain)
        res = res.split('/')[0]
        if res.find('?') > 0:
            res = res.split('?')[0]
        if res.find(':') >= 0:
            res = res.split(':')[0]
        return res

    """
    获取域名后缀
    """
    def get_postfix(cls, domain):
        if not domain:
            return None
        res = cls._clear_info(domain)
        postfix = cls._get_postfix(res)
        if not postfix or postfix == 'error':
            return None
        return postfix

    def get_topdomain(cls, domain):
        if not domain:
            return None
        res = cls._clear_info(domain)
        postfix = cls._get_postfix(res)
        if postfix:
            if postfix == 'error':
                return None
            pattern = r'[^\.]+%s$' % (postfix)
            result = re.findall(pattern, res, re.IGNORECASE)
            if result:
                return result[0]
        else:
            return '.'.join(domain.split('.')[-2:])

    def sxGetDomain(self, url):
        url = self.removeCharacters(url)
        if url.find("www.") > -1 and url.startswith("www."):
            url = url[4:]
        if url.find("/") > -1:
            url = url[0: url.rindex("/")]
        top_domain = self.get_topdomain(url)
        return top_domain if top_domain else ""

    def removeCharacters(self, previou_url):
        if previou_url.startswith("https://"):
            previou_url = previou_url.replace("https://", "")
        if previou_url.startswith("http://"):
            previou_url = previou_url.replace("http://", "")
        if previou_url.endswith("/"):
            previou_url = previou_url[0:len(previou_url) - 1]
        return previou_url


def test():
    sx = SeoDomain()

    # "http://www.51job.com/careerpost/jianlishuoming/image_class_3_65.html"
    # "http://www.unileverfoodsolutions.com.cn/content/ufs/zh/recipes/hongyundangtou.html"
    print sx.get_second_domain("http://www.shpengsen.com")

    print sx.get_second_domain("https://www.cnblogs.com/wushuaishuai/p/7686756.html")
    print sx.get_second_domain("http://su.58.com/")
    # print sx.sxGetDomain("http://www.shpengsen.com")
    print sx.get_second_domain("http://www.daqianduan.com")

    # urls = ["http://meiwen.me/src/index.html",
    #         "http://1000chi.com/game/index.html",
    #         "http://see.xidian.edu.cn/cpp/html/1429.html",
    #         "https://docs.python.org/2/howto/regex.html",
    #         """https://www.google.com.hk/search?client=aff-cs-360chromium&hs=TSj&q=url%E8%A7%A3%E6%9E%90%E5%9F%9F%E5%90%8Dre&oq=url%E8%A7%A3%E6%9E%90%E5%9F%9F%E5%90%8Dre&gs_l=serp.3...74418.86867.0.87673.28.25.2.0.0.0.541.2454.2-6j0j1j1.8.0....0...1c.1j4.53.serp..26.2.547.IuHTj4uoyHg""",
    #         "file:///D:/code/echarts-2.0.3/doc/example/tooltip.html",
    #         "http://api.mongodb.org/python/current/faq.html#is-pymongo-thread-safe",
    #         "https://pypi.python.org/pypi/publicsuffix/",
    #         "http://127.0.0.1:8000",
    #         "http://www.hao123jdjd.p",
    #         "http://tool.chinaz.com/Tools/... "
    #         ]
    # for domain in urls:
    #     # try:
    #     #     domain = get_tld(url)
    #     #     domain_list = domain.split(".")
    #     #     print domain_list[0]
    #     # except Exception as e:
    #     #     print "unkonw"
    #
    #     o = sx.sxGetDomain(domain)
    #     print o
    # print sx.sxGetDomain("http://m.baidu.com/s?word=%E8%8B%8F%E5%B7%9E")
if __name__ == '__main__':
    test()
