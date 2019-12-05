# -*- coding: UTF-8 -*-

import urllib2
import sys
import time
import traceback
# from sx_util.baidu_id_build import Baidu_id_build
import random

reload(sys)
sys.setdefaultencoding('utf8')


class GetReal_Address(object):
    """
        获取真实url
    """

    def __int__(self):
        self.ua = [
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36",
            "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:2.0b8pre) Gecko/20101114 Firefox/4.0b8pre",
            "Mozilla/5.0 (X11; U; Linux i686; it-IT; rv:1.9.0.2) Gecko/2008092313 Ubuntu/9.25 (jaunty) Firefox/3.8",
            "Mozilla/5.0 (Windows; U; Windows NT 6.1; cs; rv:1.9.2.4) Gecko/20100513 Firefox/3.6.4 (.NET CLR 3.5.30729)",
            "Mozilla/5.0 (Windows; U; Windows NT 6.0; fr; rv:1.9.2.28) Gecko/20120306 Firefox/3.6.28"]

    def findReal_Address_improve(self, url, domain=""):
        # st = time.time()

        redirect_handler = UnRedirectHandler()
        result = {"url": ""}
        result["redirect_url"] = ""
        request = urllib2.Request(url)
        opener = urllib2.build_opener(redirect_handler)
        # self.get_result(opener, request, 1, True, domain, result, temp_url=url, task_url=url)

        self.get_result_two(opener, request, result, 1, True, url, 1, domain)
        opener.close()

        r_data = result["redirect_url"] if result["redirect_url"] else result["url"]
        return r_data

    def get_result_two(self, opener, request, result, redirect, flag, task_url, redirect_index, domain):
        for i in range(0, 2):
            if not flag or redirect_index > 5:
                # print redirect_index
                return flag
            else:
                redirect_index += 1
                try:
                    response = opener.open(request, timeout=3)
                    if isinstance(response, tuple):
                        # header = response[2]
                        result["status"] = "2"
                        result["redirect_url"] = self.get_redirect_url(response[0], task_url)

                        result["code"] = response[1]
                        headers = {}
                        if "User-agent" in request.headers.keys():
                            headers["User-agent"] = request.headers.get("User-agent")
                        # if "Set-Cookie" in header:
                        #     headers["Cookie"] = header.get("Set-Cookie")
                        request = urllib2.Request(result["redirect_url"], headers=headers)
                        flag = self.get_result_two(opener, request, result, redirect, flag, result["redirect_url"],
                                               redirect_index, result["redirect_url"])
                    else:
                        body = response.read()
                        if body.find("window.location.replace") > -1:
                            direct_url = self.cut_word(body)
                            result["url"] = direct_url

                            request = urllib2.Request(direct_url)
                            flag = self.get_result_two(opener, request, result, redirect, flag, direct_url, redirect_index, result["redirect_url"])

                        return False
                except urllib2.HTTPError, e:
                    # print traceback.format_exc()
                    result["code"] = e.code
                    result["redirect_url"] = domain
                    return False
                except Exception, e:
                    # print traceback.format_exc()
                    result["redirect_url"] = domain
                    return False
        return False

    @staticmethod
    def get_redirect_url(location, task_url):
        """
            拼接url
        :param location:
        :param task_url:
        :return:
        """
        try:
            location = str(location)
            if location.startswith("http"):
                redirect_url = location
            else:
                onesplit = str(task_url).split("//")
                twosplit = str(onesplit[1]).split("/")
                site_domain = onesplit[0] + "//" + twosplit[0] + "/"
                if location.startswith("/"):
                    redirect_url = site_domain + location[1:]
                else:
                    redirect_url = site_domain + location
            return redirect_url
        except:
            return str(location)

    def cut_word(self, content):
        start_index = content.find("window.location.replace")
        temp_content = content[start_index + 25:]
        end_index = temp_content.find("\"")
        return temp_content[0: end_index]

    def findReal_Address(self, url, domain=""):
        headers = {}
        request = urllib2.Request(url, headers=headers)
        redirect_handler = UnRedirectHandler()
        opener = urllib2.build_opener(redirect_handler)
        # for i in range(0, 2):
        try:
            response = opener.open(request, timeout=10)
            # 什么情况下 是 元祖
            if isinstance(response, tuple):
                redirect_url = response[0]
                # code = response[1]
                url = self.findReal_Address(redirect_url)
        except urllib2.HTTPError:
            if domain != "":
                url = domain
        except Exception:
            if domain != "":
                url = domain
        finally:
            opener.close()
            return url


class UnRedirectHandler(urllib2.HTTPRedirectHandler):
    def __init__(self):
        pass

    def http_error_302(self, req, fp, code, msg, headers):
        if 'location' in headers:
            newurl = headers.getheaders('location')[0]
            return newurl, code, headers
        pass

    http_error_301 = http_error_303 = http_error_307 = http_error_302


def Main():
    # "https://www.baidu.com/link?url=e1JarOqqIqL4UxLgf7fAqanFOJsefI5HKhvsrwxJ82TPGzCgIpiWUetA0Z5uiKpctQ2VhcYdWkSSqIEX0aQh2aR85Ifp2VQDIcYma-JmLiKsOt1sD3-m-DUPenlcm_Hd&wd=&eqid=cd338e5600012cd9000000055885dd86"
    sx = GetReal_Address()

    # 百度文库 内部跳转
    # "http://www.baidu.com/link?url=mCIVN6nm4gys5J66NOgeQW67AfFj34EUhyL1RnU2cIQotpP_kx_aiJqRgpvgi9ouS13q1kGPqOvJbpyK9hBj66xBljoyi8oul6k-5lkud1W"
    # "http://www.baidu.com/link?url=hL-4vhy1PNAyW7ffmD5LZah018LgVN8LFuhVV6eZI43B4gEadU_lUmQ2yTH2FGF5"
    # "https://www.baidu.com/link?url=Eex7G3SjW1fEYlEzNQb6SPxSB-KP6Q-RJLtOQ0wKBwjd0jE98cfiqLlxFugBuUZTXB2N6T8h92ZchPjBboZ7JzKS3idkjxq2qdKGlgChaXkJITtTvlvRkGshEI8KdgLV&wd=&eqid=8b97121f0000246a00000005591e63e6"
    # "http://www.baidu.com/link?url=Fjxtvw1xc54CYcI0JZClotEMRT7qkXc0T2Y33IoomVrNJgkPVRF1F3qSWaTdV0r6iocOaS0by6XIzjWCr8yG4R5WWl2xYRGaapZ2F3F6iXB39UQ7Q4NrwBUBgRbMJdo2"
    # "http://www.baidu.com/link?url=Fjxtvw1xc54CYcI0JZClotEMRT7qkXc0T2Y33IoomVrNJgkPVRF1F3qSWaTdV0r6iocOaS0by6XIzjWCr8yG4R5WWl2xYRGaapZ2F3F6iXB39UQ7Q4NrwBUBgRbMJdo2"
    xx = sx.findReal_Address_improve(
        "http://www.baidu.com/link?url=M5ZS7oJgljtttuP8z4afM56382w2_bJQ0AG6ryzBkfE43bO5LiGB9TjLgCd9qrjFk-BbDGubp910bq7gvZhfSAb29HQoyKLgzuqH8kIoxjC",
        "wwwww")
    print "-----------"
    print xx


if __name__ == '__main__':
    Main()
