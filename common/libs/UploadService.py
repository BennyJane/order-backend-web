# -*- coding: utf-8 -*-
# @Time : 2020/10/24
# @Author : Benny Jane
# @Email : 暂无
# @File : __init__.py.py
# @Project : order-backend-web
import datetime
import os
import stat
import uuid

from flask import current_app
from werkzeug.utils import secure_filename

from _compat import win
from common.libs.Helper import getCurrentDate
from common.models.Image import Image
from web.extensions import db


class UploadService(object):
    @staticmethod
    def uploadByFile(file):
        app_config = current_app.config
        config_upload = app_config["UPLOAD"]
        resp = {"code": 200, "msg": "操作成功", "data": ""}
        filename = secure_filename(file.filename)
        ext = os.path.splitext(filename)[1].lstrip(".")
        if ext not in config_upload['ext']:
            resp['code'] = -1
            resp['msg'] = "不允许的扩展类型文件"
        else:
            if win:
                root_path = current_app.root_path + config_upload['win_prefix_path']
            else:
                root_path = current_app.root_path + config_upload['prefix_path']
            file_dir = datetime.datetime.now().strftime('%Y%m%d')
            save_dir = os.path.join(root_path, file_dir)
            if not os.path.exists(save_dir):
                os.mkdir(save_dir)
                if not win:
                    # linux 下修改权限: RWX 读写执行权限，  USR GRP OTH
                    os.chmod(save_dir, stat.S_IRWXU | stat.S_IRGRP | stat.S_IRWXO)
            #  图片重命名
            filename = str(uuid.uuid4()).replace("-", "") + "." + ext
            final_path = os.path.join(save_dir, filename)
            file.save(final_path)

            # 信息出入数据库
            model_image = Image()
            # 图片名 + 文件夹的名称
            dir_image = file_dir + '/' + filename  # todo 这里是拼URL，而不是文件路径
            model_image.file_key = dir_image
            model_image.created_time = getCurrentDate()  # 该时间应该设置为数据库自动添加
            db.session.add(model_image)
            db.session.commit()
            resp['data'] = {
                'file_key': model_image.file_key
            }
        return resp
