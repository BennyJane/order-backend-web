# -*- coding: utf-8 -*-
# @Time : 2020/10/23
# @Author : Benny Jane
# @Email : 暂无
# @File : __init__.py.py
# @Project : order-backend-web
import datetime

from flask import Blueprint

from common.libs.Helper import getFormatDate, ops_render
from common.models.stat.StatDailySite import StatDailySite

index_bp = Blueprint('index_page', __name__)


@index_bp.route("/")
def index():
    # 先把页面数据结构定义好
    # 这个页面就没有预设报错信息
    resp_data = {
        'data': {
            'finance': {
                'today': 0,
                'month': 0
            },
            'member': {
                'today_new': 0,
                'month_new': 0,
                'total': 0
            },
            'order': {
                'today': 0,
                'month': 0
            },
            'shared': {
                'today': 0,
                'month': 0
            },
        }
    }

    now = datetime.datetime.now()
    # 获取30天前的时间点，使用datetime库
    date_before_30days = now + datetime.timedelta(days=-30)
    date_from = getFormatDate(date=date_before_30days, format="%Y-%m-%d")
    date_to = getFormatDate(date=now, format="%Y-%m-%d")

    stat_res = StatDailySite.query.filter(StatDailySite.date >= date_from)\
        .filter(StatDailySite.date <= date_to).order_by(StatDailySite.id.asc())\
        .all()

    # 避免过多缩进
    if not stat_res:
        return ops_render("index/index.html", **resp_data)
    data = resp_data['data']
    for item in stat_res:
        data['finance']['month'] += item.total_pay_money
        data['member']['month_new'] += item.total_new_member_count
        data['member']['total'] = item.total_member_count
        data['order']['month'] += item.total_order_count
        data['shared']['month'] += item.total_shared_count
        if getFormatDate(date=item.date, format="%Y-%m-%d") == date_to:  # 获取当天的数据
            data['finance']['today'] = item.total_pay_money
            data['member']['today_new'] = item.total_new_member_count
            data['order']['today'] = item.total_order_count
            data['shared']['today'] = item.total_shared_count
    return ops_render("index/index.html", **resp_data)
