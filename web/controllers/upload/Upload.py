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
from common.libs.UploadService import UploadService
from common.libs.UrlManager import UrlManager
from common.libs.validators import ParamsValidator
from common.models.Image import Image

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
    resp = {'state': 'SUCCESS', 'url': '', 'title': '', 'original': ''}
    file_target = request.files
    upfile = file_target['upfile'] if 'upfile' in file_target else None
    if upfile is None:
        resp['state'] = "上传失败"
        return jsonify(resp)
    ret = UploadService.uploadByFile(upfile)
    if ret['code'] != 200:
        ret = UploadService.uploadByFile(upfile)['code'] != 200
        resp['state'] = "上传失败：" + ret['msg']
    else:
        resp['url'] = UrlManager.buildImageUrl(ret['data']['file_key'])
    return jsonify(resp)


def listImage():
    resp = {'state': 'SUCCESS', 'list': [], 'start': 0, 'total': 0}

    req = request.values
    page_size = ParamsValidator.GetORSetValue(req, 'size', value=20)
    start = ParamsValidator.GetORSetValue(req, 'start', value=0)

    query = Image.query
    if start > 0:
        query = query.filter(Image.id < start)
    res_list = query.order_by(Image.id.desc()).limit(page_size).all()
    images = []
    if res_list:
        for item in res_list:
            images.append({'url': UrlManager.buildImageUrl(item.file_key)})
            start = item.id
    resp['list'] = images
    resp['start'] = start  # 该数值？？
    resp['total'] = len(images)
    return jsonify(resp)
