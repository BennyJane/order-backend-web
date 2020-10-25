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
        result = src[target] if target in src else value
        # 根据value的值，判断输入内容的类型
        try:
            if isinstance(value, int):
                result = int(result)
            elif isinstance(value, float):
                result = float(result)
        except Exception:
            pass
        return result
