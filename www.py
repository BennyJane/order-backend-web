# -*- coding: utf-8 -*-
# @Time : 2020/10/23
# @Author : Benny Jane
# @Email : 暂无
# @File : application.py
# @Project : order-backend-web

from web.controllers.index import index_bp
# from web.controllers.static import static_bp
from web.controllers.user.User import user_bp
from web.controllers.chart import chart_bp
from web.controllers.account.Account import account_bp


def register_blueprint(app):
    app.register_blueprint(index_bp, url_prefix='/')
    app.register_blueprint(user_bp, url_prefix='/user')
    app.register_blueprint(chart_bp, url_prefix='/chart')
    app.register_blueprint(account_bp, url_prefix='/account')
    # app.register_blueprint(static_bp, url_prefix='/static')
