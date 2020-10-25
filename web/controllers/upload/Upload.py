# -*- coding: utf-8 -*-
# @Time : 2020/10/24
# @Author : Benny Jane
# @Email : 暂无
# @File : __init__.py.py
# @Project : order-backend-web
import json
import re

from flask import Blueprint, request, current_app, jsonify

from _compat import win

upload_bp = Blueprint('upload_page', __name__)


@upload_bp.route('/ueditor', methods=['get', 'post'])
def ueditor():
    req = request.values
    action = req['action'] if 'action' in req else ""

    if action == 'config':
        root_path = current_app.root_path
        if win:
            config_path = "{0}/web/static/plugins/ueditor/upload_config.json".format(root_path)
        else:
            config_path = "{0}\\web\\static\\plugins\\ueditor\\upload_config.json".format(root_path)
        with open(config_path, encoding='utf-8') as f:
            try:
                config_data = json.loads(re.sub(r'\/\*.*\*/', '', f.read()))
            except Exception:
                config_data = {}
        return jsonify(config_data)

    if action == "uploadimage":
        return uploadImage()

    if action == "listimage":
        return listImage()

    return "upload"


@upload_bp.route("/pic", methods=["GET", "POST"])
def uploadPic():
    file_target = request.files
    upfile = file_target['pic'] if 'pic' in file_target else None
    callback_target = 'window.parent.upload'
    if upfile is None:
        return "<script type='text/javascript'>{0}.error('{1}')</script>".format(callback_target, "上传失败")

    ret = UploadService.uploadByFile(upfile)
    if ret['code'] != 200:
        return "<script type='text/javascript'>{0}.error('{1}')</script>".format(callback_target, "上传失败：" + ret['msg'])

    return "<script type='text/javascript'>{0}.success('{1}')</script>".format(callback_target, ret['data']['file_key'])


def uploadImage():
    pass


def listImage():
    pass
