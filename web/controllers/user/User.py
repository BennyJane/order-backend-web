# -*- coding: utf-8 -*-
# @Time : 2020/10/24
# @Author : Benny Jane
# @Email : 暂无
# @File : __init__.py.py
# @Project : order-backend-web
import json

from flask import Blueprint, request, g, redirect, jsonify, make_response, current_app

from common.libs.Helper import ops_render
from common.libs.UrlManager import UrlManager
from common.libs.user.UserService import UserService
from common.libs.validators import ParamsValidator
from common.models.User import User
from web.extensions import db

user_bp = Blueprint('user_page', __name__)


@user_bp.route('/login', methods=['get', 'post'])
def login():
    if request.method == 'GET':  # 优先判断逻辑简单的情况
        if g.get("current_user", None):
            return redirect(UrlManager.buildUrl("/"))
        return ops_render('user/login.html')
    resp = {"code": 200, "msg": "登录成功", "data": {}}
    req = request.values  # 通过values获取post数据
    login_name = req["login_name"] if "login_name" in req else ""
    login_pwd = req["login_pwd"] if "login_pwd" in req else ""

    if ParamsValidator.DataRequired(login_name):
        resp['code'] = -1
        resp['msg'] = "请输入正确的登录用户名"
        return jsonify(resp)
    if ParamsValidator.DataRequired(login_pwd):
        resp['code'] = -1
        resp['msg'] = "请输入正确的邮箱密码"
        return jsonify(resp)

    user_info = User.query.filter_by(login_name=login_name).one_or_none()
    if not user_info:
        resp['code'] = -1
        resp['msg'] = "请输入正确的登录用户名"
        return jsonify(resp)

    if user_info.login_pwd != UserService.genePwd(login_pwd, user_info.login_salt):
        resp['code'] = -1
        resp['msg'] = "请输入正确的密码"
        return jsonify(resp)

    if user_info.status != 1:
        resp['code'] = -1
        resp['msg'] = "账号已被禁用，请联系管理员处理"
        return jsonify(resp)

    response = make_response(json.dumps(resp))
    response.set_cookie(current_app.config['AUTH_COOKIE_NAME'],
                        "{}#{}".format(UserService.geneAuthCode(user_info), user_info.uid), 60 * 60 * 24 * 120)
    return response


@user_bp.route('/edit', methods=['get', 'post'])
def edit():
    if request.method == "GET":
        return ops_render('user/edit.html', current="edit")

    resp = {'code': 200, 'msg': '操作成功~', 'data': {}}
    req = request.values
    nickname = req.get('nickname', "")
    email = req.get('email', "")

    # 这儿的逻辑判断： 只要出现错误，就更新resp，并退出； 只有没有错误的时候，才会执行else
    if ParamsValidator.DataRequired(nickname):
        resp['code'] = -1
        resp['msg'] = "请输入符合规范的姓名"
    elif ParamsValidator.DataRequired(email):
        resp['code'] = -1
        resp['msg'] = "请输入符合规范的邮箱"
    else:
        user_info = g.current_user
        user_info.nickname = nickname
        user_info.email = email
        db.session.add(user_info)
        db.session.commit()
    return jsonify(resp)


@user_bp.route('/reset-pwd', methods=['get', 'post'])
def resetPwd():
    if request.method == 'GET':
        return ops_render("user/reset_pwd.html", current="reset-pwd")
    resp = {'code': 200, 'msg': '操作成功~', 'data': {}}
    req = request.values

    old_password = req.get("old_password", "")
    new_password = req.get("new_password", "")

    user_info = g.current_user

    if ParamsValidator.DataRequired(old_password):
        resp['code'] = -1
        resp['msg'] = "请输入符合规范的原密码"
    elif ParamsValidator.DataRequired(new_password):
        resp['code'] = -1
        resp['msg'] = "请输入符合规范的新密码"
    elif old_password == new_password:
        resp['code'] = -1
        resp['msg'] = "新密码和原密码不能相同, 请重新输入"
    elif user_info.uid == 1:
        resp['code'] = -1
        resp['msg'] = "该用户是演示账号，不准修改密码和登录用户名"
    else:
        user_info.login_pwd = UserService.genePwd(new_password, user_info.login_salt)

        db.session.add(user_info)
        db.session.commit()

        # todo 封装成组件
        response = make_response(json.dumps(resp))
        # 重新设置了cookie
        response.set_cookie(current_app.config['AUTH_COOKIE_NAME'], '%s#%s' % (
            UserService.geneAuthCode(user_info), user_info.uid), 60 * 60 * 24 * 120)  # 保存120天

    return jsonify(resp)


@user_bp.route('/logout')
def logout():
    response = make_response(UrlManager.buildUrl("/user/login"))
    # 清空cookie内在字段
    response.delete_cookie(current_app.config['AUTH_COOKIE_NAME'])
    return response
