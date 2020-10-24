# -*- coding: utf-8 -*-
# @Time : 2020/10/24
# @Author : Benny Jane
# @Email : 暂无
# @File : validators.py
# @Project : order-backend-web

class ParamsValidator:
    def __init__(self):
        pass

    @staticmethod
    def DataRequired(target):
        return target is None or len(target) < 1
