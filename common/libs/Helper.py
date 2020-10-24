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
