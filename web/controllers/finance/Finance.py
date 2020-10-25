# -*- coding: utf-8 -*-
# @Time : 2020/10/24
# @Author : Benny Jane
# @Email : 暂无
# @File : __init__.py.py
# @Project : order-backend-web
import json

from flask import Blueprint, request, current_app, redirect, jsonify
from sqlalchemy import func

from common.libs.Helper import iPagination, selectFilterObj, getDictListFilterField, ops_render, getDictFilterField, \
    getCurrentDate
from common.libs.UrlManager import UrlManager
from common.libs.validators import ParamsValidator
from common.models.food.Food import Food
from common.models.member.Member import Member
from common.models.pay.PayOrder import PayOrder
from common.models.pay.PayOrderItem import PayOrderItem
from web.extensions import db

finance_bp = Blueprint('finance_page', __name__)


@finance_bp.route('/index')
def index():
    resp_data = {}
    req = request.values

    page = int(req['p']) if ('p' in req and req['p']) else 1
    # 1：支付完成 0 无效 -1 申请退款 -2 退款中 -9 退款成功  -8 待支付  -7 完成支付待确认
    status = ParamsValidator.GetORSetValue(req, 'status', value="")

    query = PayOrder.query
    if status and int(status) > -1:
        query = query.filter(PayOrder.status == int(req['status']))

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
    pay_list = query.order_by(PayOrder.id.desc()).offset(offset).limit(app_config['PAGE_SIZE']).all()
    data_list = []
    # todo 梳理逻辑
    if pay_list:
        # 将订单号全部取出来
        pay_order_ids = selectFilterObj(pay_list, "id")
        # todo 修改为连表查询 ==》 优化sql性能
        # 获取订单id 对应的订单数据
        pay_order_items_map = getDictListFilterField(PayOrderItem, PayOrderItem.pay_order_id, "pay_order_id",
                                                     pay_order_ids)

        food_mapping = {}
        if pay_order_items_map:
            food_ids = []
            for item in pay_order_items_map:
                tmp_food_its = selectFilterObj(pay_order_items_map[item], 'food_id')
                # todo ??
                tmp_food_its = {}.fromkeys(tmp_food_its).keys()
                food_ids = food_ids + list(tmp_food_its)
            # food_ids里面会有重复的，要去重 todo
            food_mapping = getDictListFilterField(Food, Food.id, 'id', food_ids)

        for item in pay_list:
            tmp_data = {
                "id": item.id,
                "status_desc": item.status_desc,
                "order_number": item.order_number,
                "price": item.total_price,
                "pay_time": item.pay_time,
                "created_time": item.created_time.strftime("%Y%m%d%H%M%S")
            }
            tmp_foods = []
            tmp_order_items = pay_order_items_map[item.id]
            for tmp_order_item in tmp_order_items:
                tmp_food_info = food_mapping[tmp_order_item.food_id]
                tmp_foods.append({
                    'name': tmp_food_info.name,
                    'quantity': tmp_order_item.quantity
                })
            tmp_data['foods'] = tmp_foods
            data_list.append(tmp_data)

    resp_data['list'] = data_list
    resp_data['pages'] = pages
    resp_data['search_con'] = req
    resp_data['pay_status_mapping'] = current_app.config['PAY_STATUS_MAPPING']
    resp_data['current'] = 'index'
    return ops_render("finance/index.html", **resp_data)


@finance_bp.route('/pay-info')
def info():
    resp_data = {}
    req = request.values
    input_id = int(req['id']) if 'id' in req else 0

    reback_url = UrlManager.buildUrl("/finance/index")

    if input_id < 1:
        return redirect(reback_url)
    pay_order_info = PayOrder.query.filter_by(input_id=input_id).first()
    if not pay_order_info:
        return redirect(reback_url)

    # 订单对应的会员信息
    member_info = Member.query.filter_by(id=pay_order_info.member_id).first()
    if not member_info:
        return redirect(reback_url)
    # 查找订单对应的商品列表
    order_item_list = PayOrderItem.query.filter_by(pay_order_id=pay_order_info.id).all()
    data_order_item_list = []
    if order_item_list:
        food_map = getDictFilterField(Food, Food.id, "id", selectFilterObj(order_item_list, "food_id"))
        for item in order_item_list:
            tmp_food_info = food_map[item.food_id]
            tmp_data = {
                "quantity": item.quantity,
                "price": item.price,
                "name": tmp_food_info.name
            }
            data_order_item_list.append(tmp_data)

    address_info = {}
    if pay_order_info.express_info:
        address_info = json.loads(pay_order_info.express_info)
    resp_data['pay_order_info'] = pay_order_info
    resp_data['pay_order_items'] = data_order_item_list
    resp_data['member_info'] = member_info
    resp_data['address_info'] = address_info
    resp_data['current'] = 'index'
    return ops_render("finance/pay_info.html", **resp_data)


@finance_bp.route("/account")
def finance_set():
    resp_data = {}
    req = request.values
    page = int(req['p']) if ('p' in req and req['p']) else 1
    query = PayOrder.query.filter_by(status=1)

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
    res_list = query.order_by(PayOrder.id.desc()).offset(offset).limit(app_config['PAGE_SIZE']).all()

    stat_info = db.session.query(PayOrder, func.sum(PayOrder.total_price).label("total")) \
        .filter(PayOrder.status == 1).first()

    current_app.logger.info(stat_info)
    resp_data['list'] = res_list
    resp_data['pages'] = pages
    resp_data['total_money'] = stat_info[1] if stat_info[1] else 0.00
    resp_data['current'] = 'account'
    return ops_render("finance/account.html", **resp_data)


# todo 该接口用途
@finance_bp.route("/ops", methods=["POST"])
def orderOps():
    resp = {'code': 200, 'msg': '操作成功~', 'data': {}}
    req = request.values
    input_id = ParamsValidator.GetORSetValue(req, 'id', value=0)
    act = ParamsValidator.GetORSetValue(req, 'act', value="")
    pay_order_info = PayOrder.query.filter_by(id=input_id).first()
    if not pay_order_info:
        resp['code'] = -1
        resp['msg'] = "系统繁忙。请稍后再试"
    elif act == "express":
        pay_order_info.express_status = -6
        pay_order_info.updated_time = getCurrentDate()
        db.session.add(pay_order_info)
        db.session.commit()

    return jsonify(resp)
