# -*- coding: utf-8 -*-
# @Time : 2020/10/24
# @Author : Benny Jane
# @Email : 暂无
# @File : __init__.py.py
# @Project : order-backend-web
from decimal import Decimal

from flask import Blueprint, request, current_app, redirect, jsonify
from sqlalchemy import or_

from common.libs.Helper import iPagination, getDictFilterField, ops_render, getCurrentDate
from common.libs.UrlManager import UrlManager
from common.libs.food.FoodService import FoodService
from common.libs.validators import ParamsValidator
from common.models.food.Food import Food
from common.models.food.FoodCat import FoodCat
from common.models.food.FoodStockChangeLog import FoodStockChangeLog
from web.extensions import db

food_bp = Blueprint('food_page', __name__)


@food_bp.route('/index')
def index():
    resp_data = {}
    req = request.values
    page = request.args.get('p', 1, type=int)
    mix_kw = ParamsValidator.GetORSetValue(req, 'mix_kw',value="")
    # 状态 1：有效 0：无效
    status = ParamsValidator.GetORSetValue(req, 'status', value=None)
    cat_id = ParamsValidator.GetORSetValue(req, 'cat_id', value="")

    query = Food.query

    if mix_kw:
        rule = or_(Food.name.ilike(f"%{mix_kw}%"), Food.tags.ilike(f"%{mix_kw}%"))
        query = query.filter(rule)
    if status and int(status) > -1:
        query = query.filter(Food.status == int(status))

    if cat_id and int(cat_id) > 0:
        query = query.filter(Food.cat_id == int(cat_id))

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
    res_list = query.order_by(Food.id.desc()).offset(offset).limit(app_config['PAGE_SIZE']).all()

    cat_mapping = getDictFilterField(FoodCat, FoodCat.id, "id", [])  # 获取FoodCat所有内容
    resp_data['list'] = res_list
    resp_data['pages'] = pages
    resp_data['search_con'] = req
    resp_data['status_mapping'] = app_config['STATUS_MAPPING']
    resp_data['cat_mapping'] = cat_mapping
    resp_data['current'] = 'index'
    return ops_render("food/index.html", **resp_data)


@food_bp.route("/info")
def info():
    resp_data = {}
    input_id = request.args.get('id', 0, type=int)
    reback_url = UrlManager.buildUrl("/food/index")

    if input_id < 1:
        return redirect(reback_url)

    target_info = Food.query.filter_by(id=input_id).first()
    if not target_info:
        return redirect(reback_url)

    stock_change_list = FoodStockChangeLog.query.filter(FoodStockChangeLog.food_id == input_id) \
        .order_by(FoodStockChangeLog.id.desc()).all()

    resp_data['info'] = target_info
    resp_data['stock_change_list'] = stock_change_list
    resp_data['current'] = 'index'
    return ops_render("food/info.html", **resp_data)


@food_bp.route("/set", methods=['GET', 'POST'])
def foot_set():
    # 修改食物库存等信息
    if request.method == "GET":
        resp_data = {}
        input_id = request.args.get('id', 0, type=int)
        target_info = Food.query.filter_by(id=input_id).first()
        if target_info and target_info.status != 1:
            return redirect(UrlManager.buildUrl("/food/index"))

        cat_list = FoodCat.query.all()
        resp_data['info'] = target_info
        resp_data['cat_list'] = cat_list
        resp_data['current'] = 'index'
        return ops_render("food/set.html", **resp_data)

    resp = {'code': 200, 'msg': '操作成功~~', 'data': {}}
    req = request.values
    input_id = ParamsValidator.GetORSetValue(req, 'id', value=0)
    cat_id = ParamsValidator.GetORSetValue(req, 'cat_id', value=0)
    name = ParamsValidator.GetORSetValue(req, 'name', value="")
    price = ParamsValidator.GetORSetValue(req, 'price', value="")
    main_image = ParamsValidator.GetORSetValue(req, 'main_image', value="")
    summary = ParamsValidator.GetORSetValue(req, 'summary', value="")
    stock = ParamsValidator.GetORSetValue(req, 'stock', value=0)
    tags = ParamsValidator.GetORSetValue(req, 'tags', value="")

    converted_price = 0.00
    try:
        converted_price = Decimal(price).quantize(Decimal('0.00'))
    except Exception:
        pass
    if cat_id < 1:
        resp['code'] = -1
        resp['msg'] = "请选择分类~~"
    elif name is None or len(name) < 1:
        resp['code'] = -1
        resp['msg'] = "请输入符合规范的名称"
    elif not price or len(price) < 1:
        resp['code'] = -1
        resp['msg'] = "请输入符合规范的售卖价格"
    elif converted_price <= 0:
        resp['code'] = -1
        resp['msg'] = "请输入符合规范的售卖价格"
    elif main_image is None or len(main_image) < 3:
        resp['code'] = -1
        resp['msg'] = "请上传封面图"
    elif summary is None or len(summary) < 3:
        resp['code'] = -1
        resp['msg'] = "请输入食物描述，并不能少于10个字符"
    elif stock < 1:
        resp['code'] = -1
        resp['msg'] = "请输入符合规范的库存量"
    elif tags is None or len(tags) < 1:
        resp['code'] = -1
        resp['msg'] = "请输入标签，便于搜索"
    else:
        food_info = Food.query.filter_by(id=input_id).first()
        before_stock = 0
        if food_info:
            model_food = food_info
            before_stock = model_food.stock
        else:
            # 创建新对象
            model_food = Food()
            model_food.status = 1
            model_food.created_time = getCurrentDate()
        model_food.cat_id = cat_id
        model_food.name = name
        model_food.price = price
        model_food.main_image = main_image
        model_food.summary = summary
        model_food.stock = stock
        model_food.tags = tags
        model_food.updated_time = getCurrentDate()

        db.session.add(model_food)
        db.session.commit()

        FoodService.setStockChangeLog(model_food.id, int(stock) - int(before_stock), "后台修改")

    return jsonify(resp)


@food_bp.route("/cat")
def cat():
    # 显示食物分类
    resp_data = {}
    req = request.values
    query = FoodCat.query

    if 'status' in req and int(req['status']) > -1:
        query = query.filter(FoodCat.status == int(req['status']))
    app_config = current_app.config
    res_list = query.order_by(FoodCat.weight.desc(), FoodCat.id.desc()).all()
    resp_data['list'] = res_list
    resp_data['search_con'] = req
    resp_data['status_mapping'] = app_config['STATUS_MAPPING']
    resp_data['current'] = 'cat'
    return ops_render("food/cat.html", **resp_data)


# 修改食物分类信息
@food_bp.route("/cat-set", methods=["GET", "POST"])
def catSet():
    if request.method == "GET":
        resp_data = {}
        input_id = request.args.get('id', 0, type=int)
        target_info = None
        if input_id:
            target_info = FoodCat.query.filter_by(id=input_id).first()
        resp_data['info'] = target_info
        resp_data['current'] = 'cat'
        return ops_render("food/cat_set.html", **resp_data)

    resp = {'code': 200, 'msg': '操作成功', 'data': {}}
    req = request.values

    input_id = ParamsValidator.GetORSetValue(req, 'id', value=0)
    name = ParamsValidator.GetORSetValue(req, 'name', value="")
    weight = int(req['weight']) if ('weight' in req and int(req['weight']) > 0) else 1

    if name is None or len(name) < 1:
        resp['code'] = -1
        resp['msg'] = "请输入符合规范的分类名称"
    else:
        food_cat_info = FoodCat.query.filter_by(id=input_id).first()
        if food_cat_info:
            model_food_cat = food_cat_info
        else:
            model_food_cat = FoodCat()
            model_food_cat.created_time = getCurrentDate()
        model_food_cat.name = name
        model_food_cat.weight = weight
        model_food_cat.updated_time = getCurrentDate()
        db.session.add(model_food_cat)
        db.session.commit()
    return jsonify(resp)


# 修改分类信息展示页面
@food_bp.route("/cat-ops", methods=["POST"])
def catOps():
    resp = {'code': 200, 'msg': '操作成功', 'data': {}}
    req = request.values

    input_id = ParamsValidator.GetORSetValue(req, 'id', value=0)
    act = ParamsValidator.GetORSetValue(req, 'act', value="")

    food_cat_info = FoodCat.query.filter_by(id=input_id).first()

    if not input_id:
        resp['code'] = -1
        resp['msg'] = "请选择要操作的账号"
    elif act not in ['remove', 'recover']:
        resp['code'] = -1
        resp['msg'] = "操作有误，请重试"
    elif not food_cat_info:
        resp['code'] = -1
        resp['msg'] = "指定分类不存在"
    else:
        if act == "remove":
            food_cat_info.status = 0
        elif act == "recover":
            food_cat_info.status = 1
            food_cat_info.update_time = getCurrentDate()
        db.session.add(food_cat_info)
        db.session.commit()
    return jsonify(resp)


'''
小程序使用的接口

'''


@food_bp.route("/ops", methods=["POST"])
def ops():
    resp = {'code': 200, 'msg': '操作成功', 'data': {}}
    req = request.values

    input_id = ParamsValidator.GetORSetValue(req, 'id', value=0)
    act = ParamsValidator.GetORSetValue(req, 'act', value="")

    if not input_id:
        resp['code'] = -1
        resp['msg'] = "请选择要操作的账号"
    elif act not in ['remove', 'recover']:
        resp['code'] = -1
        resp['msg'] = "操作有误，请重试"
    elif not Food.query.filter_by(id=id).one_or_none():
        resp['code'] = -1
        resp['msg'] = "指定美食不存在"
    else:
        food_info = Food.query.filter_by(id=id).one_or_none()
        if act == "remove":
            food_info.status = 0
        elif act == "recover":
            food_info.status = 1
        food_info.updated_time = getCurrentDate()
        db.session.add(food_info)
        db.session.commit()
    return jsonify(resp)
