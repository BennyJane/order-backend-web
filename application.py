# -*- coding: utf-8 -*-
# @Time : 2020/10/23
# @Author : Benny Jane
# @Email : 暂无
# @File : application.py
# @Project : order-backend-web
import os

from flask_script import Manager

from _compat import win
from common.libs.UrlManager import UrlManager
from web.app import Application
from web.extensions import db
from web.interceptors.ErrorInterceptor import register_error
from www import register_blueprint

base_dir = os.path.abspath(os.path.dirname(__file__))

if win:
    template_folder = os.path.join(base_dir, f"web\\templates\\")
    static_folder = os.path.join(base_dir, f"web\\static\\")
    # todo 考虑配置文件导入，放在Application类之中
    base_config = os.path.join(base_dir, f"config\\base_setting.py")
    env_config = os.path.join(base_dir, f"config\\{os.getenv('FLASK_CONFIG', 'local_setting')}.py")
else:
    template_folder = os.path.join(base_dir, f"web/templates/")
    static_folder = os.path.join(base_dir, f"web/static/")
    base_config = os.path.join(base_dir, f"config/base_setting.py")
    env_config = os.path.join(base_dir, f"config/{os.getenv('FLASK_CONFIG', 'local_setting')}.py")

app = Application(__name__, template_folder=template_folder, root_path=os.getcwd(), static_folder=static_folder)
app.config.from_pyfile(base_config)
app.config.from_pyfile(env_config)
db.init_app(app)
register_blueprint(app)
register_error(app)

app.add_template_global(UrlManager.buildUrl, 'buildUrl')
app.add_template_global(UrlManager.buildStaticUrl, 'buildStaticUrl')
app.add_template_global(UrlManager.buildImageUrl, 'buildImageUrl')

# Manager 没有init__app() 方法
manager = Manager(app)
