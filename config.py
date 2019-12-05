# -*- coding: utf8 -*-

baidu_spider_move = {
    'host': '47.104.129.13',
    'user': 'fxt',
    'password': 'xiaowei1',
    'db': 'sub_xiala_monitor'
}

qcloud_cos = {
    'secret_id': 'AKIDuDIrPvhqd9UTZ3NjiUdfS2RM6fhTl8rW',  # 替换为用户的 secretId
    'secret_key': '2ewHzQjg4sSv9D1asABDK9a8OmytaQQJ',  # 替换为用户的 secretKey
    'region': 'ap-shanghai',  # 替换为用户的 Region
    'token': None,  # 使用临时密钥需要传入 Token，默认为空，可不填
    'scheme': 'https',  # 指定使用 http/https 协议来访问 COS，默认为 https，可不填
    'bucket': 'fxt-monitor-1251174242',  # bucket-appid
    'prefix': 'dev'
}

callback_url = "http://xiaowei.winndoo.cn/receiveData"

# 重查次数
search_count = 20

# 查词开始时间/结束时间
time_now = "09:00:00"
time_now_end = "17:00:00"

# 是否发送数据到cos
is_send_html_to_cos = False

# 排名
reach_rank = 10
