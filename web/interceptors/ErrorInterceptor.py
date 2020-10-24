# -*- coding: utf-8 -*-
# @Time : 2020/10/23
# @Author : Benny Jane
# @Email : 暂无
# @File : __init__.py.py
# @Project : order-backend-web
from common.libs.Helper import ops_render
from common.libs.LogService import LogService


def register_error(app):
    @app.errorhandler(404)
    def error_404(e):
        LogService.addErrorLog(str(e))
        return ops_render('error/error.html', status=404, msg="很抱歉！您访问的页面不存在")
