# -*- coding: utf-8 -*-
# @Time : 2020/10/24
# @Author : Benny Jane
# @Email : 暂无
# @File : validators.py
# @Project : order-backend-web

class ParamsValidator(object):
    def __init__(self):
        pass

    @staticmethod
    def DataRequired(target):
        return target is None or len(target) < 1

    @staticmethod
    def GetORSetValue(src, target, value=None):
        """
        value 默认设置为空字符串
        """
        if value is None:
            value = ""
        return src[target] if target in src else value
