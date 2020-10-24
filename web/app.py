# -*- coding: utf-8 -*-
# @Time : 2020/10/23
# @Author : Benny Jane
# @Email : 暂无
# @File : app.py
# @Project : order-backend-web

from flask import Flask

# from .extensions import db


class Application(Flask):
    def __int__(self, import_name, template_folder=None, root_path=None, static_folder=None):
        # static_folder 设置为None的时候，可以取消内置的 static 视图函数
        # static_folder: 默认是 app.root_path + '/static'; 当修改
        super(Application, self).__init__(import_name, template_folder=template_folder, root_path=root_path,
                                          static_folder=static_folder)
        # 添加扩展 todo  配置文件的加载放到了实例化以后，所以添加扩展也需要往后放
        # db.init_app(self)
