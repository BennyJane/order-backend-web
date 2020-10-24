# -*- coding: utf-8 -*-
# @Time : 2020/10/23
# @Author : Benny Jane
# @Email : 暂无
# @File : base_config.py
# @Project : order-backend-web

DEBUG = True
FLASK_ENV = 'development'
SQLALCHEMY_ECHO = True
# SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(base_dir, 'FLogin.sqlite')

# SQLALCHEMY_DATABASE_URI = 'mysql://root:123456@127.0.0.1/order_web?charset=utf8mb4'
SQLALCHEMY_DATABASE_URI = 'mysql://root:123456@127.0.0.1/food_db?charset=utf8mb4'
SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_ENCODING = "utf8mb4"
