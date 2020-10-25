# -*- coding: utf-8 -*-
# @Time : 2020/10/24
# @Author : Benny Jane
# @Email : 暂无
# @File : __init__.py.py
# @Project : order-backend-web

# 统计管理页面
import datetime

from flask import Blueprint, request, current_app

from common.libs.Helper import getFormatDate, iPagination, ops_render, getDictFilterField, selectFilterObj
from common.models.food.Food import Food
from common.models.member.Member import Member
from common.models.stat.StatDailyFood import StatDailyFood
from common.models.stat.StatDailyMember import StatDailyMember
from common.models.stat.StatDailySite import StatDailySite

stat_bp = Blueprint('stat_page', __name__)


@stat_bp.route("/index")
def index():
    now = datetime.datetime.now()
    date_before_30days = now + datetime.timedelta(days=-30)
    default_date_from = getFormatDate(date=date_before_30days, format="%Y-%m-%d")
    default_date_to = getFormatDate(date=now, format="%Y-%m-%d")

    resp_data = {}
    req = request.values
    page = int(req['p']) if ('p' in req and req['p']) else 1
    date_from = req['date_from'] if 'date_from' in req else default_date_from
    date_to = req['date_to'] if 'date_to' in req else default_date_to
    query = StatDailySite.query.filter(StatDailySite.date >= date_from) \
        .filter(StatDailySite.date <= date_to)

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

    res_list = query.order_by(StatDailySite.id.desc()).offset(offset).limit(app_config['PAGE_SIZE']).all()
    resp_data['list'] = res_list
    resp_data['pages'] = pages
    resp_data['current'] = 'index'
    resp_data['search_con'] = {
        'date_from': date_from,
        'date_to': date_to
    }
    return ops_render("stat/index.html", **resp_data)


@stat_bp.route("/food")
def food():
    now = datetime.datetime.now()
    date_before_30days = now + datetime.timedelta(days=-30)
    default_date_from = getFormatDate(date=date_before_30days, format="%Y-%m-%d")
    default_date_to = getFormatDate(date=now, format="%Y-%m-%d")

    resp_data = {}
    req = request.values
    page = int(req['p']) if ('p' in req and req['p']) else 1
    date_from = req['date_from'] if 'date_from' in req else default_date_from
    date_to = req['date_to'] if 'date_to' in req else default_date_to
    query = StatDailyFood.query.filter(StatDailyFood.date >= date_from) \
        .filter(StatDailyFood.date <= date_to)

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

    res_list = query.order_by(StatDailyFood.id.desc()).offset(offset).limit(app_config['PAGE_SIZE']).all()
    date_list = []
    if res_list:
        food_map = getDictFilterField(Food, Food.id, "id", selectFilterObj(res_list, "food_id"))
        for item in res_list:
            tmp_food_info = food_map[item.food_id] if item.food_id in food_map else {}
            tmp_data = {
                "date": item.date,
                "total_count": item.total_count,
                "total_pay_money": item.total_pay_money,
                'food_info': tmp_food_info
            }
            date_list.append(tmp_data)

    resp_data['list'] = date_list
    resp_data['pages'] = pages
    resp_data['current'] = 'food'
    resp_data['search_con'] = {
        'date_from': date_from,
        'date_to': date_to
    }
    return ops_render("stat/food.html", **resp_data)


@stat_bp.route("/member")
def memebr():
    now = datetime.datetime.now()
    date_before_30days = now + datetime.timedelta(days=-30)
    default_date_from = getFormatDate(date=date_before_30days, format="%Y-%m-%d")
    default_date_to = getFormatDate(date=now, format="%Y-%m-%d")

    resp_data = {}
    req = request.values
    page = int(req['p']) if ('p' in req and req['p']) else 1
    date_from = req['date_from'] if 'date_from' in req else default_date_from
    date_to = req['date_to'] if 'date_to' in req else default_date_to
    query = StatDailyMember.query.filter(StatDailyMember.date >= date_from) \
        .filter(StatDailyMember.date <= date_to)

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

    res_list = query.order_by(StatDailyMember.id.desc()).offset(offset).limit(app_config['PAGE_SIZE']).all()
    date_list = []
    if res_list:
        member_map = getDictFilterField(Member, Member.id, "id", selectFilterObj(res_list, "member_id"))
        for item in res_list:
            tmp_member_info = member_map[item.member_id] if item.member_id in member_map else {}
            tmp_data = {
                "date": item.date,
                "total_pay_money": item.total_pay_money,
                "total_shared_count": item.total_shared_count,
                'member_info': tmp_member_info
            }
            date_list.append(tmp_data)

    resp_data['list'] = date_list
    resp_data['pages'] = pages
    resp_data['current'] = 'member'
    resp_data['search_con'] = {
        'date_from': date_from,
        'date_to': date_to
    }
    return ops_render("stat/member.html", **resp_data)


@stat_bp.route("/share")
def share():
    now = datetime.datetime.now()
    date_before_30days = now + datetime.timedelta(days=-30)
    default_date_from = getFormatDate(date=date_before_30days, format="%Y-%m-%d")
    default_date_to = getFormatDate(date=now, format="%Y-%m-%d")

    resp_data = {}
    req = request.values
    page = int(req['p']) if ('p' in req and req['p']) else 1
    date_from = req['date_from'] if 'date_from' in req else default_date_from
    date_to = req['date_to'] if 'date_to' in req else default_date_to
    query = StatDailySite.query.filter(StatDailySite.date >= date_from) \
        .filter(StatDailySite.date <= date_to)

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

    res_list = query.order_by(StatDailySite.id.desc()).offset(offset).limit(app_config['PAGE_SIZE']).all()
    resp_data['list'] = res_list
    resp_data['pages'] = pages
    resp_data['current'] = 'food'
    resp_data['search_con'] = {
        'date_from': date_from,
        'date_to': date_to
    }
    return ops_render("stat/share.html", **resp_data)
