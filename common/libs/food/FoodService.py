# -*- coding: utf-8 -*-
# @Time : 2020/10/24
# @Author : Benny Jane
# @Email : 暂无
# @File : __init__.py.py
# @Project : order-backend-web
from common.libs.Helper import getCurrentDate
from common.models.food.FoodStockChangeLog import FoodStockChangeLog
from web.controllers.food import Food
from web.extensions import db


class FoodService(object):

    @staticmethod
    def setStockChangeLog(food_id=0, quantity=0, note=''):

        if food_id < 1:
            return False

        food_info = Food.query.filter_by(id=food_id).first()
        if not food_info:
            return False

        model_stock_change = FoodStockChangeLog()
        model_stock_change.food_id = food_id
        model_stock_change.unit = quantity
        model_stock_change.total_stock = food_info.stock
        model_stock_change.note = note
        model_stock_change.created_time = getCurrentDate()
        db.session.add(model_stock_change)
        db.session.commit()
        return True
