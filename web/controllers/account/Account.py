# -*- coding: utf-8 -*-
# @Time : 2020/10/24
# @Author : Benny Jane
# @Email : 暂无
# @File : __init__.py.py
# @Project : order-backend-web

from flask import Blueprint, request, current_app, redirect, jsonify
from sqlalchemy import or_

from common.libs.Helper import iPagination, ops_render, getCurrentDate
from common.libs.UrlManager import UrlManager
from common.libs.user.UserService import UserService
from common.libs.validators import ParamsValidator
from common.models.User import User
from common.models.log.AppAccessLog import AppAccessLog
from web.extensions import db

account_bp = Blueprint('account_page', __name__)


@account_bp.route('/index')
def index():
    resp_data = {}
    req = request.values
    page = int(req['p']) if ('p' in req and req['p']) else 1
    mix_kw = req.get('mix_kw', None)
    status = req.get('status', None)
    query = User.query

    if mix_kw:
        rule = or_(User.nickname.ilike("%{}%".format(mix_kw)), User.mobile.ilike("%{}%".format(mix_kw)))
        query = query.filter(rule)
    if status and int(status) > -1:
        query = query.filter(User.status == int(status))

    # 获取app的配置文件
    app_config = current_app.config

    page_params = {
        'total': query.count(),
        'page_size': app_config['PAGE_SIZE'],
        'page': page,
        'display': app_config['PAGE_DISPLAY'],
        'url': request.full_path.replace("&p={}".format(page), "")
    }
    pages = iPagination(page_params)
    offset = (page - 1) * app_config['PAGE_SIZE']
    limit = app_config['PAGE_SIZE'] * page

    res_list = query.order_by(User.uid.desc()).all()[offset:limit]

    resp_data['list'] = res_list
    resp_data['pages'] = pages
    resp_data['search_con'] = req
    resp_data['status_mapping'] = app_config['STATUS_MAPPING']
    # todo 不要将这些变量拆分为单个的健值对，传入模板中； 不方便写注释
    return ops_render("account/index.html", **resp_data)


@account_bp.route('/info')
def info():
    req = request.args
    uid = int(req.get('id'), 0)
    reback_url = UrlManager.buildUrl("/account/index")
    if uid < 1:
        return redirect(reback_url)
    info = User.query.filter_by(uid=uid).one_or_none()
    if not info:
        return redirect(reback_url)

    access_list = AppAccessLog.query.filter_by(uid=uid).order_by(AppAccessLog.id.desc()).limit(10).all()
    return ops_render('account/info.html', info=info, access_list=access_list)


@account_bp.route("/set", methods=["GET", "POST"])
def setPwd():
    default_pwd = "******"
    if request.method == 'GET':
        req = request.args
        uid = int(req.get('id'), 0)
        info = None
        if uid:
            info = User.query.filter_by(uid=uid).one_or_none()
        return ops_render("account/set.html", info=info)

    resp = {'code': 200, 'msg': '操作成功', 'data': {}}
    req = request.values
    # 尽量不要使用id作为变量名， 内建函数 id（）
    user_id = ParamsValidator.GetORSetValue(req, 'id', value=0)
    nickname = ParamsValidator.GetORSetValue(req, 'nickname')
    mobile = ParamsValidator.GetORSetValue(req, 'mobile')
    email = ParamsValidator.GetORSetValue(req, 'email')
    login_name = ParamsValidator.GetORSetValue(req, 'login_name')
    login_pwd = ParamsValidator.GetORSetValue(req, 'login_pwd')

    if ParamsValidator.DataRequired(nickname):
        resp['code'] = -1
        resp['msg'] = "请输入符合规范的姓名"
    elif ParamsValidator.DataRequired(mobile):
        resp['code'] = -1
        resp['msg'] = "请输入符合规范的手机号码"
    elif ParamsValidator.DataRequired(email):
        resp['code'] = -1
        resp['msg'] = "请输入符合规范的邮箱"
    elif ParamsValidator.DataRequired(login_name):
        resp['code'] = -1
        resp['msg'] = "请输入符合规范的登录用户名"
    elif ParamsValidator.DataRequired(login_pwd):
        resp['code'] = -1
        resp['msg'] = "请输入符合规范的登录密码"
    elif User.query.filter(User.login_name == login_name, User.uid != user_id).one_or_none():
        resp['code'] = -1
        resp['msg'] = "该登录名已存在，请换一个试试"
    else:
        user_info = User.query.filter_by(uid=user_id).first()
        if user_info:
            model_user = user_info
        else:
            model_user = User()
            model_user.created_time = getCurrentDate()
            model_user.login_salt = UserService.geneSalt()
        model_user.nickname = nickname
        model_user.mobile = mobile
        model_user.email = email
        model_user.login_name = login_name
        if login_pwd != default_pwd:
            if user_info and user_info.uid == 1:
                resp['code'] = -1
                resp['msg'] = "该用户是演示账号，不准修改密码和登录用户名"
                return jsonify(resp)
            # 当前密码 等于 默认密码的时候， 不更新密码  todo 只有输入密码不等于默认密码的时候才更新密码
            model_user.login_pwd = UserService.genePwd(login_pwd, model_user.login_salt)
        model_user.updated_time = getCurrentDate()
        db.session.add(model_user)
        db.session.commit()

    return jsonify(resp)


@account_bp.route("/ops", methods=["POST"])
def ops():
    resp = {'code': 200, 'msg': '操作成功', 'data': {}}
    req = request.values

    user_id = ParamsValidator.GetORSetValue(req, 'id', value=0)
    act = ParamsValidator.GetORSetValue(req, 'act')
    user_info = User.query.filter_by(uid=id).first()

    if ParamsValidator.DataRequired(user_id):
        resp['code'] = -1
        resp['msg'] = "请选择要操作的账号"
    elif act not in ['remove', 'recover']:
        resp['code'] = -1
        resp['msg'] = "操作有误，请重试"
    elif not user_info:
        resp['code'] = -1
        resp['msg'] = "指定账号不存在"
    elif user_info and user_info.uid == 1:
        resp['code'] = -1
        resp['msg'] = "该用户是演示账号，不准操作账号"
    else:
        if act == "remove":
            user_info.status = 0
        elif act == "recover":
            user_info.status = 1
        user_info.update_time = getCurrentDate()
        db.session.add(user_info)
        db.session.commit()
    return jsonify(resp)
