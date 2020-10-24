# -*- coding: utf-8 -*-
# @Time : 2020/10/23
# @Author : Benny Jane
# @Email : 暂无
# @File : __init__.py.py
# @Project : order-backend-web

from flask import Blueprint, send_from_directory, current_app

static_bp = Blueprint('static', __name__)

# todo 和这个没有什么关系
# 这个文件是为了解决开发模式下，静态文件找不到的bug 《== 该bug 来自于使用了 url管理器方法
# 线上部署不需要改文件
@static_bp.route("/<path:filename>")
def index(filename):
    print("==== static", filename)
    # 这里要在application内设置root_path， 并覆盖默认static
    return send_from_directory(current_app.root_path + "/web/static" + filename)

