# -*- coding: utf-8 -*-
# @Time : 2020/10/23
# @Author : Benny Jane
# @Email : 暂无
# @File : base_config.py
# @Project : order-backend-web

SERVER_PORT = 8002
DEBUG = False
SQLALCHEMY_ECHO = False

AUTH_COOKIE_NAME = "order_food"

SEO_TITLE = "好吃点快餐厅"
IGNORE_URLS = [
    "^/user/login"
]

IGNORE_CHECK_LOGIN_URLS = [
    "^/static",
    "^/favicon.ico"
]

API_IGNORE_URLS = [
    "^/api"
]

PAGE_SIZE = 50
PAGE_DISPLAY = 10

STATUS_MAPPING = {
    "1": "正常",
    "0": "已删除"
}

MAIN_APP = {
    'appid': 'wxcb87d24a0b5ac827',
    'appkey': '12bdff874fa92e8a15c1fbf1403c32ca',
    'paykey': 'xxxxxxxxxxxxxx换自己的',
    'mch_id': 'xxxxxxxxxxxx换自己的',
    'callback_url': '/api/order/callback'
}

UPLOAD = {
    'ext': ['jpg', 'gif', 'bmp', 'jpeg', 'png'],
    # windows 下 与linux 的文件路径不同
    # linux
    'prefix_path':'/web/static/upload/',
    'prefix_url':'/static/upload/',
    # windows
    'win_prefix_path': "\\web\\static\\upload",
    'win_prefix_url': "\\static\\upload\\"
}

APP = {
    "domain": f'http://127.0.0.1:{SERVER_PORT}'
}

PAY_STATUS_MAPPING = {
    "1": "已支付",
    "-8": "待支付",
    "0": "已关闭"
}

PAY_STATUS_DISPLAY_MAPPING = {
    "0": "订单关闭",
    "1": "支付成功",
    "-8": "待支付",
    "-7": "待发货",
    "-6": "待确认",
    "-5": "待评价"
}
