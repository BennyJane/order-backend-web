# -*- coding: utf-8 -*-
# @Time : 2020/10/23
# @Author : Benny Jane
# @Email : 暂无
# @File : __init__.py
# @Project : order-backend-web
import sys

plat = sys.platform

win = False

if plat.startswith('win'):
    win = True
