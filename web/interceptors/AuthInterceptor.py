# -*- coding: utf-8 -*-
# @Time : 2020/10/23
# @Author : Benny Jane
# @Email : 暂无
# @File : __init__.py.py
# @Project : order-backend-web
import re

from flask import request, g, redirect, current_app

from common.libs.LogService import LogService
from common.libs.UrlManager import UrlManager
from common.libs.user.UserService import UserService
from common.models.User import User

'''
可以实现的方法：
1. 懒加载
def register_before_request(app):
    @app.before_request
    def check()
        pass
2.直接调用 app.before_request(f())
'''


def check_auth():
    ignore_urls = current_app.config['IGNORE_URLS']
    ignore_check_login_urls = current_app.config['IGNORE_CHECK_LOGIN_URLS']
    path = request.path

    # 如果是静态文件就不要查询用户信息了
    pattern = re.compile('%s' % "|".join(ignore_check_login_urls))
    if pattern.match(path):
        return

    if '/api' in path:
        return

    user_info = check_login()
    g.current_user = None
    if user_info:
        g.current_user = user_info

    # 加入日志
    LogService.addAccessLog()
    pattern = re.compile('%s' % "|".join(ignore_urls))
    if pattern.match(path):
        return

    if not user_info:
        return redirect(UrlManager.buildUrl("/user/login"))

    return


def check_login():
    auth_cookie = None
    cookies = request.cookies
    AUTH_COOKIE_NAME = current_app.config.get('AUTH_COOKIE_NAME', None)
    if AUTH_COOKIE_NAME is not None:
        auth_cookie = cookies.get(AUTH_COOKIE_NAME, None)

    # 处理api接口
    if '/api' in request.path:
        current_app.logger.info(request.path)
        auth_cookie = request.headers.get("Authorization")
        current_app.logger.info(request.headers.get("Authorization"))

    if auth_cookie is None:
        return False

    # 参考User模块内 AUTH_COOKIE_NAME 值的设置
    auth_info = auth_cookie.split("#")
    if len(auth_info) != 2:
        return False

    # 该变量的定义
    try:
        user_info = User.query.filter_by(uid=auth_info[1]).first()
    except Exception:
        return False

    if user_info is None:
        return False

    if auth_info[0] != UserService.geneAuthCode(user_info):
        return False

    if user_info.status != 1:
        return False

    return user_info
