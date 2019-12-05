# -*- coding: utf8 -*-

from download_center.new_spider.downloader.downloader import SpiderRequest
from download_center.new_spider.spider.basespider import BaseSpider
from download_center.new_spider.downloader.downloader import Downloader

import time
import traceback
import sys
from Queue import Empty
from datetime import datetime
import objgraph
from Queue import Queue
from threading import Thread

reload(sys)
sys.setdefaultencoding('utf8')


class BaseSpiderSign(BaseSpider):
    """
    将处理结果和存储结果模块分别独立出来的爬虫类
    BaseSpiderSeparateDeal，处理结果线程deal_response只负责解析结果，解析完成后将待存储的数据放入store_queue队列里面，
    等待存储结果线程store_results去处理

    Args:
        headers: 字典，http头信息，
            举例，{'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:47.0) Gecko/20100101 Firefox/47.0'}
        config: 字典，可为空，用于向下载中心发送优先级、并发数等相关信息，
            举例：{'concurrent_num':0, 'priority':2, expire_time: '2016-08-08 12:00:00', 'store_type': 3,
                   'redirect': 0, 'post_data': {}, 'param': {'capture_width': 1024, 'capture_height': 768}}
            conf_district_id 表示为地域，默认为0，即不指定地域，具体值参考district表
        urls: 数组，将要抓取的url及类型、过期时间等
            [{'url': 'http://www.baidu.com', 'type': 1},
            {'url': 'http://www.sina.com', 'type': 2}]
            unique_key 和 url 组成唯一值  作为下载中心去重

        __record_user_task  记录向下载中心发送的任务量 , 如果status为3,任务多  相当于 一个任务查3 次
        store_type: 1：结果存储mysql， 2：结果存储redis，3：结果存储elasticsearch

    """

    def __init__(self):
        super(BaseSpiderSign, self).__init__()
        self.sended_tasks_max = 4000    # 限制发送队列 到达限制 待发送队列将持续增大,注意限制待发送队列 大小
        self.log = None
        # self.conf_store_type = 1      # 指定 下载存储类型 1:数据库 2:redis  默认1 不用
        self.conf_finish_state = True   # True 当所有队列长度为0时停止,  False 一直运行， 默认有终止
        self.url_repeat = True          # 默认重复的url重发 false 不重发
        self.response_queue_max = 1000   # response_queue 队列大小
        # self.sending_queue = Queue()

    def send_requests(self, max_idle_time):
        """
        发送请求。将sending_queue队列中的SpiderRequest对象通过downloader发送到下载中心
        这边限制发送任务数
        """
        downloader = self.get_downloader()
        start_time = time.time()
        while True:
            try:
                if self.sended_queue.qsize() < self.sended_tasks_max \
                        and self.response_queue.qsize() < self.sended_tasks_max:
                    request = self.sending_queue.get_nowait()
                    if request.user_id is None:
                        request.user_id = self.user_id
                    results = downloader.set(request)
                    self.deal_request_results(request, results)
                    start_time = time.time()
                    self.send_wait()
                else:
                    time.sleep(10)
            except Empty:
                if max_idle_time == -1:
                    pass
                elif start_time + max_idle_time < time.time():
                    if self.is_finish():
                        break
                time.sleep(10)
            except Exception:
                print traceback.format_exc()

    def get_response(self, max_idle_time):
        """
        获取url爬取结果。将sended_queue队列中的SpiderRequest对象通过downloader到下载中心去获取抓取到的html
        """
        downloader = self.get_downloader()
        start_time = time.time()
        while True:
            try:
                if self.response_queue.qsize() < self.response_queue_max:
                    request = self.sended_queue.get_nowait()
                    results = downloader.get(request)
                    self.response_queue.put((request, results))
                    start_time = time.time()
                    # self.get_wait()
                else:
                    time.sleep(10)
            except Empty:
                if max_idle_time == -1:
                    pass
                elif start_time + max_idle_time < time.time():
                    if self.is_finish():
                        break
                time.sleep(10)
            except Exception, e1:
                print(traceback.format_exc())

    @staticmethod
    def integer_point():
        """
            获取当前时间的小时数
        :return:
        """
        return int(time.strftime('%H', time.localtime(time.time())))

    def record_log(self, idle=1):
        """
            5 分钟打印一次 日志
            记录抓取日志，用于调整各个线程参数设置
        """
        while True:
            print('time_now:%s; sending_queue:%d; sended_queue:%d; response_queue:%d; store_queue:%d'
                  % (str(datetime.today()), self.sending_queue.qsize(), self.sended_queue.qsize(),
                     self.response_queue.qsize(), self.store_queue.qsize()))
            objgraph.show_most_common_types()
            time.sleep(300)
            if self.is_finish():
                break

    def deal_response_results(self, request, results, stores):
        if results == 0:
            print "deal_response_results results = 0 "
            return False
        else:
            urls = list()       # 重新去获取的url
            failed_urls = list()    # 失败重发的url
            for u in request.urls:
                url = u['unique_md5']
                if url in results:
                    result = results[url]
                    task_status = str(result['status'])
                    if task_status in ['2', '3']:
                        if result.get("es_status", "") == 1:
                            print "deal_response_results results = 1 es get exception"
                            failed_urls.append(u)
                        else:
                            ret_failed_urls = self.deal_response_results_status(task_status, u, result, request)
                            if ret_failed_urls:
                                failed_urls = failed_urls + ret_failed_urls
                    else:
                        urls.append(u)
                else:
                    self.log.error('url send failure unique_md5:{}; url have:{}'.format(url, u["url"]))
                    if self.url_repeat:
                        failed_urls.append(u)
            if len(urls) > 0:
                request.urls = urls
                self.sended_queue.put(request)
            if len(failed_urls) > 0:
                new_request = SpiderRequest(headers=request.headers, config=request.config)
                # new_request = copy(request)
                new_request.urls = failed_urls
                self.sending_queue.put(new_request)
                new_request = None

    def deal_response_results_status(self, task_status, url, result, request):
        """
            处理 task_status 是2,3的任务  重试返回数组， 若重试需切换headers内容需自行定义
        :param task_status:
        :param url:
        :param result:
        :param request:
        :return:
        """
        raise NotImplementedError()

    def deal_request_results(self, request, results):
        if results == 0:
            self.log.error('params exception request failure urls: %s' % request.urls)
            # self.sended_queue.put(request)
        elif results == -2:
            self.log.error('没有相应地域 urls: %s' % request.urls)
        elif results == -1:
            # 网络原因或锁表
            self.log.error("向数据库 添加任务失败  设置request 失败  urls: %s" % request.urls)
            self.sended_queue.put(request)
        else:
            self.sended_queue.put(request)

    def is_finish(self):
        if self.conf_finish_state:
            return self.sending_queue.qsize() == 0 and self.sended_queue.qsize() == 0 \
                   and self.response_queue.qsize() == 0 and self.store_queue.qsize() == 0
        else:
            return False

    @staticmethod
    def retry(u, count):
        retry_urls = list()
        if "conf_search_count" in u:
            if int(u["conf_search_count"]) <= int(count):
                u["conf_search_count"] = int(u["conf_search_count"]) + 1
                retry_urls.append(u)
            else:
                print "conf_search_count > %s url:%s" % (str(count), u["url"])
                # self.log_record.info("conf_search_count > 3 url:%s" % u)
        else:
            u["conf_search_count"] = 1
            retry_urls.append(u)
        return retry_urls
