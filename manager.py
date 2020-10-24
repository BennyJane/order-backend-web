# -*- coding: utf-8 -*-
# @Time : 2020/10/23
# @Author : Benny Jane
# @Email : 暂无
# @File : application.py
# @Project : order-backend-web
from flask_script import Server

from application import app, manager

manager.add_command('runserver',
                    Server(host="127.0.0.1", port=app.config['SERVER_PORT'], use_debugger=True, use_reloader=True))


def main():
    manager.run()


if __name__ == '__main__':
    try:
        import sys

        sys.exit(main())
    except Exception as e:
        import traceback

        traceback.print_exc()
