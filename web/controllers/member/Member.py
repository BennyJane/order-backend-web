# -*- coding: utf-8 -*-
# @Time : 2020/10/24
# @Author : Benny Jane
# @Email : 暂无
# @File : __init__.py.py
# @Project : order-backend-web
from flask import Blueprint, request, current_app, redirect, jsonify

from common.libs.Helper import iPagination, ops_render, getCurrentDate, getDictFilterField, selectFilterObj
from common.libs.UrlManager import UrlManager
from common.libs.validators import ParamsValidator
from common.models.food.Food import Food
from common.models.member.Member import Member
from common.models.member.MemberComments import MemberComments
from common.models.pay.PayOrder import PayOrder
from web.extensions import db

member_bp = Blueprint('member_page', __name__)


@member_bp.route("/index")
def index():
    resp_data = {}
    req = request.values
    page = int(req['p']) if ('p' in req and req['p']) else 1
    mix_kw = ParamsValidator.GetORSetValue(req, 'mix_kw')
    # 状态 1：有效 0：无效
    status = ParamsValidator.GetORSetValue(req, 'status', value=None)
    query = Member.query

    if mix_kw:
        query = query.filter(Member.nickname.ilike(f"%{mix_kw}%"))

    if status and int(status) > -1:
        query = query.filter(Member.status == int(status))

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
    res_lsit = query.order_by(Member.id.desc()).offset(offset).limit(app_config['PAGE_SIZE']).all()

    resp_data['list'] = res_lsit
    resp_data['pages'] = pages
    resp_data['search_con'] = req
    resp_data['status_mapping'] = app_config['STATUS_MAPPING']
    resp_data['current'] = 'index'
    return ops_render("member/index.html", **resp_data)


# 显示会员个人信息
@member_bp.route("/info")
def info():
    resp_data = {}
    req = request.args
    id = int(req.get("id", 0))
    reback_url = UrlManager.buildUrl("/member/index")
    if id < 1:
        return redirect(reback_url)

    target_info = Member.query.filter_by(id=id).first()
    if not target_info:
        return redirect(reback_url)
    # 查找会员的订单列表
    pay_order_list = PayOrder.query.filter_by(member_id=id).filter(PayOrder.status.in_([-8, 1])) \
        .order_by(PayOrder.id.desc()).all()
    # 评论列表
    comment_list = MemberComments.query.filter_by(member_id=id).order_by(MemberComments.id.desc()).all()

    resp_data['info'] = target_info
    resp_data['pay_order_list'] = pay_order_list
    resp_data['comment_list'] = comment_list
    resp_data['current'] = 'index'
    return ops_render("member/info.html", **resp_data)


# 修改会员的信息
@member_bp.route("/set", methods=["GET", "POST"])
def set():
    if request.method == "GET":
        resp_data = {}
        input_id = request.args.get("id", 0, type=int)
        reback_url = UrlManager.buildUrl("/member/index")
        if input_id < 1:
            return redirect(reback_url)

        target_info = Member.query.filter_by(id=input_id).first()
        if not target_info:
            return redirect(reback_url)

        if target_info.status != 1:
            return redirect(reback_url)

        resp_data['info'] = target_info
        resp_data['current'] = 'index'
        return ops_render("member/set.html", **resp_data)

    resp = {'code': 200, 'msg': '操作成功', 'data': {}}
    req = request.values
    input_id = ParamsValidator.GetORSetValue(req, 'id', value=0)
    nickname = ParamsValidator.GetORSetValue(req, 'nickname', value='')
    if nickname is None or len(nickname) < 1:
        resp['code'] = -1
        resp['msg'] = "请输入符合规范的姓名"
        return jsonify(resp)
    elif not Member.query.filter_by(id=input_id).first():
        resp['code'] = -1
        resp['msg'] = "指定会员不存在"
    else:
        member_info = Member.query.filter_by(id=input_id).first()
        member_info.nickname = nickname
        member_info.updated_time = getCurrentDate()
        db.session.add(member_info)
        db.session.commit()
    return jsonify(resp)


@member_bp.route("/comment")
def comment():
    resp_data = {}
    req = request.args
    page = int(req['p']) if ('p' in req and req['p']) else 1
    query = MemberComments.query

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

    comment_list = query.order_by(MemberComments.id.desc()).offset(offset).limit(app_config['PAGE_SIZE']).all()
    data_list = []
    if comment_list:
        member_map = getDictFilterField(Member, Member.id, "id", selectFilterObj(comment_list, "member_id"))
        food_ids = []
        for item in comment_list:
            tmp_food_ids = (item.food_ids[1:-1]).split("_")
            tmp_food_ids = {}.fromkeys(tmp_food_ids).keys()
            food_ids = food_ids + list(tmp_food_ids)

        food_map = getDictFilterField(Food, Food.id, "id", food_ids)

        for item in comment_list:
            # todo 思考这儿的技巧
            tmp_member_info = member_map[item.member_id]
            tmp_foods = []
            tmp_food_ids = (item.food_ids[1:-1]).split("_")
            for tmp_food_id in tmp_food_ids:
                tmp_food_info = food_map[int(tmp_food_id)]
                tmp_foods.append({
                    'name': tmp_food_info.name,
                })

            tmp_data = {
                "content": item.content,
                "score": item.score,
                "member_info": tmp_member_info,
                "foods": tmp_foods
            }
            data_list.append(tmp_data)
    resp_data['list'] = data_list
    resp_data['pages'] = pages
    resp_data['current'] = 'comment'

    return ops_render("member/comment.html", **resp_data)


@member_bp.route("/ops", methods=["POST"])
def ops():
    resp = {'code': 200, 'msg': '操作成功~~', 'data': {}}
    req = request.values

    id = ParamsValidator.GetORSetValue(req, 'id', value=0)
    act = ParamsValidator.GetORSetValue(req, 'mix_kw', value="")

    if not id:
        resp['code'] = -1
        resp['msg'] = "请选择要操作的账号"
    elif act not in ['remove', 'recover']:
        resp['code'] = -1
        resp['msg'] = "操作有误，请重试"
    elif not Member.query.filter_by(id=id).first():
        resp['code'] = -1
        resp['msg'] = "指定会员不存在"
    else:
        member_info = Member.query.filter_by(id=id).first()
        if act == "remove":
            member_info.status = 0
        elif act == "recover":
            member_info.status = 1
        member_info.updated_time = getCurrentDate()
        db.session.add(member_info)
        db.session.commit()
    return jsonify(resp)
