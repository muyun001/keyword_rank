# -*- coding: utf-8 -*-
"""
 @Time: 2017/8/9 14:49
 @Author: sunxiang
"""
import os
import sys
import traceback
import config
from datetime import datetime, date

PROJECT_PATH = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(PROJECT_PATH)
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
reload(sys)
sys.setdefaultencoding('utf8')

from datetime import datetime
import time
import urllib
import urllib2
import json
import abc

from download_center.new_spider.downloader.downloader import SpiderRequest
from download_center.util.util_log import UtilLogger
from store.util_basestore import SourceStore
from store.rank_store import RankStore
from store.rank_history import RankHistoryStore
from util.py_store_mysql_pool import StoreMysqlPool
from util.store_type_enums import StoreTypeEnums
from util.device_enums import DeviceEnums
from util.useragent import UserAgentUtil
from spider.basespider_sign import BaseSpiderSign
import config
from qcloud_cos import CosConfig
from qcloud_cos import CosS3Client



class BaseSugRankSpider(BaseSpiderSign):
    """
        层级拓展
        完全匹配更改
        1、最靠前排名 暂存 内存  查完url 发送
        2、本地 返回真实url
    """
    search_device = None
    extractor = None

    def __init__(self):
        super(BaseSugRankSpider, self).__init__()
        # 定时休眠时间  分钟
        self.difsecond = 180
        log_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))+"/logs/"
        self.log = UtilLogger('SugSpider', log_path + 'log_sug_spider')
        self.log_record = UtilLogger('RecordSugSpider', log_path + 'log_record_sug_spider')

        self.rank_store = RankStore()
        self.history_store = RankHistoryStore()
        self.sleep_time = 60 * 15  # 没有任务休眠时间
        self.sended_queue_maxsize = 1500  # 发送限制
        self.send_one_tasks = 800  # 一次取出

        self.reset_task_time = 60 * 60  # 1小时
        # self.saveport = 3  # 端口
        self.task_table = "task"
        self.conf_finish_state = False
        self.re_send_count = 4

        self.db_pool = StoreMysqlPool(**config.baidu_spider_move)

    def get_user_password(self):
        return 'fxt', 'fxt_spider'

    def start_requests(self):
        try:
            while True:
                print(self.sended_queue.qsize())
                if self.sended_queue.qsize() < self.sended_queue_maxsize and self.sending_queue.qsize() < self.sended_queue_maxsize \
                        and self.response_queue.qsize() < self.sended_queue_maxsize and self.store_queue.qsize() < self.sended_queue_maxsize:
                    device = self.search_device.name if self.search_device != DeviceEnums.pc_360 else '360_pc'
                    task_results = self.rank_store.find_task_lists(device, self.send_one_tasks)
                    if len(task_results) > 0:
                        print "datetime:{},task_results length:{}".format(datetime.now(), len(task_results))
                        for result in task_results:
                            #  id, keyword, urlAddress, device, page, searchType, keyword_id, saveport
                            task_id = result[0]
                            keyword = result[1]
                            target_url = result[2]
                            page = result[3]
                            spidertype = result[4]
                            keyword_id = result[5]

                            req = self.get_request_param(task_id, keyword, target_url, keyword_id)
                            basic_request = SpiderRequest(urls=req['urls'], config=req['configs'])
                            self.sending_queue.put(basic_request)
                        time.sleep(20)
                    else:
                        time.sleep(self.sleep_time)
                else:
                    time.sleep(self.sleep_time)
        except Exception:
            print traceback.format_exc()

    def deal_rank_spider_response(self, url, html, ip):
        result = self.extractor.extractor(html, url['ckurl'])
        self.store_rank(url, result, html, ip)

    @abc.abstractmethod
    def get_request_param(self, task_id, keyword, target_url, keyword_id):
        """{'headers':{}, 'configs':{}, 'url':''}"""
        return

    def store_rank(self, url, rank, response_body, ip):
        item = dict()
        item["keyword"] = url["keyword"]
        item["rank"] = rank
        item["taskId"] = int(url["id"])
        item['target'] = url['ckurl']
        item["response_body"] = response_body
        item['device'] = url['search_device']
        item['ip'] = ip

        self.store_queue.put({"result": item, "task_id": url["id"], "type": StoreTypeEnums.mysql.value, "rank": rank,
                              "keyword_id": url["keyword_id"]})

    def get_stores(self):
        stores = list()
        stores.append(SourceStore(config.baidu_spider_move))
        self.stores = stores
        return stores

    def deal_response_results_status(self, task_status, url, result, request):
        if task_status == '2':
            self.deal_rank_spider_response(url, result["result"], result['inter_pro'])
        else:
            # 根据情况做处理
            self.store_rank(url, -1, result["result"], result['inter_pro'])
            self.log.info('spider failure:%s' % url)
            self.re_send(url, request)

    def re_send(self, url, request):
        self.log_record.info("re_send url:{}, User-Agent:{}".format(url["url"], request.headers["User-Agent"]))
        retry_urls = list()
        if "conf_search_count" in url:
            if int(url["conf_search_count"]) < self.re_send_count:
                url["conf_search_count"] = int(url["conf_search_count"]) + 1
                retry_urls.append(url)
            else:
                self.log_record.info(
                    "datetime:{}; state_url:{}; heasers:{}; config:{}".format(datetime.now(), url["url"],
                                                                              request.headers, request.config))
                return
        else:
            url["conf_search_count"] = 1
            retry_urls.append(url)
        new_request = SpiderRequest(headers=request.headers, config=request.config)
        new_request.urls = retry_urls
        new_request.config["priority"] = 3
        new_request.headers["User-Agent"] = UserAgentUtil().random_one(self.search_device)
        self.sending_queue.put(new_request)

    def send_response_body_cos(self, response_body, keyword_id, device, ip):
        """
        将response_body存入腾讯云
        :return:
        """
        try:
            region = config.qcloud_cos.get('region')
            app_id = config.qcloud_cos.get('app_id')
            secret_id = config.qcloud_cos.get('secret_id')
            secret_key = config.qcloud_cos.get('secret_key')
            token = config.qcloud_cos.get('token')
            scheme = config.qcloud_cos.get('scheme')
            bucket = config.qcloud_cos.get('bucket')
            prefix = config.qcloud_cos.get('prefix')
            db_name = config.baidu_spider_move.get("db")
            filename = "{prefix}/html/{date}/{device}/{db_name}/{keyword_id}_{ip}.txt".format(prefix=prefix,
                                                                                         date=date.today().isoformat(),
                                                                                         device=device,
                                                                                         db_name=db_name,
                                                                                         keyword_id=keyword_id,
                                                                                         ip=ip)
            cos_config = CosConfig(Region=region, Appid=app_id, SecretId=secret_id, SecretKey=secret_key,
                                   Token=token, Scheme=scheme)
            client = CosS3Client(cos_config)
            response = client.put_object(
                Bucket=bucket,
                Body=response_body,
                Key=filename,
                StorageClass='STANDARD',
                EnableMD5=False
            )
            print response['ETag']
        except Exception as e:
            print "save_response_body_cos error: {}".format(e)

    # @timeout(10)
    def to_store_results(self, results, stores):
        """
            results  type 1: 正常删除task 新增rank，2,3:判断, 3:有完全匹配
                    task_id  task表id
        """
        try:
            # start_time = time.time()
            task_id = results["task_id"]
            keyword_id = results["keyword_id"]
            result = results["result"]
            rank = result["rank"]
            response_body = result["response_body"]
            ip = result['ip']
            device = result['device']
            if config.is_send_html_to_cos:
                self.send_response_body_cos(response_body, keyword_id, device, ip)

            device = self.search_device.name if self.search_device != DeviceEnums.pc_360 else '360_pc'
            rank_data = [{"keywordid": keyword_id, "url": result["target"], "rank": rank,
                          "device": device, "keyword": result["keyword"]}]
            send_data = {"rankLists": json.dumps(rank_data)}
            flag = self.send_rank_data(config.callback_url, send_data)
            if flag:
                self.log_record.info("one finish keyword_id:{}, rank:{}; target: {}"
                                     .format(keyword_id, result["rank"],result.get("target", "")))
            else:
                self.log.info("send exception keyword_id:{}, send_url:{}".format(keyword_id, config.callback_url))
                # self.log.info("send exception data:{}".format(send_data))
            self.rank_store.update_status_id(task_id, result["rank"])
            self.history_store.save(self.search_device.name, keyword_id, rank)
        except:
            print traceback.format_exc()

    def send_rank_data(self, send_url, send_data):
        for i in xrange(0, 2):
            try:
                request = urllib2.Request(send_url, data=urllib.urlencode(send_data))
                response = urllib2.urlopen(request, timeout=10)
                res_content = response.read()
                if not str(res_content).find("success") > -1:
                    self.log_record.info("res_content no success send_url: {}".format(send_url))
                    return False
                return True
            except:
                self.log.info(traceback.format_exc())
                self.log.info(send_url + ",send_rank_data: " + urllib.urlencode(send_data))
                time.sleep(2)
        return False

    def reset_task(self):
        """
         重置任务表 状态
        :return:
        """
        while True:
            time.sleep(10)
            # self.log_record.info("reset:%s" % str(datetime.today()))
            self.rank_store.reset_task(self.reset_task_time)
            time.sleep(self.reset_task_time)


def Main():
    # spider = BaseSugRankSpider()
    # spider.run(8, 5, 5, 2, -1, -1, -1, -1, False)
    print(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

if __name__ == '__main__':
    Main()
