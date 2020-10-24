# -*- coding: utf-8 -*-
# @Time : 2020/10/24
# @Author : Benny Jane
# @Email : 暂无
# @File : __init__.py.py
# @Project : order-backend-web
import datetime

from flask import g, render_template

"""
统一渲染方法
不定关键字参数的合理定义方式： **kwargs; 
不合理： content={} 参数最好为不可变对象
"""


def ops_render(template, **context):
    """
    :param template: 渲染的模板路径
    :param context: 模板内传入的参数
    :return: 渲染好的模板
    """
    if "current_user" in g:
        context["current_user"] = g.get("current_user", None)
    return render_template(template, **context)


"""
获取格式化的时间
"""


def getFormatDate(date=None, format='%Y-%m-%d %H:%M:%S'):
    if date is None:
        date = datetime.datetime.now()
    return date.strftime(format)


'''
获取当前时间
'''


def getCurrentDate(format="%Y-%m-%d %H:%M:%S"):
    return datetime.datetime.now().strftime(format)
    # return datetime.datetime.now()


'''
自定义分页类
'''


def iPagination(params):
    import math

    ret = {
        "is_prev": 1,
        "is_next": 1,
        "from": 0,
        "end": 0,
        "current": 0,
        "total_pages": 0,
        "page_size": 0,
        "total": 0,
        "url": params['url']
    }

    total = int(params['total'])
    page_size = int(params['page_size'])
    page = int(params['page'])
    display = int(params['display'])  # 设置翻页器展示几个页码
    total_pages = int(math.ceil(total / page_size))  # 向上取整数
    total_pages = total_pages if total_pages > 0 else 1
    if page <= 1:
        ret['is_prev'] = 0

    if page >= total_pages:
        ret['is_next'] = 0
    # 计算页码的起始与终止位置
    semi = int(math.ceil(display / 2))

    if page - semi > 0:
        ret['from'] = page - semi
    else:
        ret['from'] = 1

    if page + semi <= total_pages:
        ret['end'] = page + semi
    else:
        ret['end'] = total_pages

    ret['current'] = page
    ret['total_pages'] = total_pages
    ret['page_size'] = page_size
    ret['total'] = total
    ret['range'] = range(ret['from'], ret['end'] + 1)  # 返回页码范围的值
    return ret
