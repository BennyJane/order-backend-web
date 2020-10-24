# -*- coding: utf-8 -*-
# @Time : 2020/10/24
# @Author : Benny Jane
# @Email : 暂无
# @File : __init__.py.py
# @Project : order-backend-web

from web.extensions import db


class Image(db.Model):
    # 只有需要定义表的名称与与类名称的小写不一致的时候，才需要使用 __tablename__
    __tablename__ = 'images'

    id = db.Column(db.Integer, primary_key=True)
    file_key = db.Column(db.String(), nullable=False, server_default=db.FetchedValue())
    created_time = db.Column(db.DateTime, nullable=False, server_default=db.FetchedValue())
