# -*- coding: utf-8 -*-
# @Time : 2020/10/23
# @Author : Benny Jane
# @Email : 暂无
# @File : extensions.py
# @Project : order-backend-web
from flask_script import Manager
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


# todo 想办法将其转化为相同接口
def init_manager(app):
    manager = Manager(app)
