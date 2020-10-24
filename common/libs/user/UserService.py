# -*- coding: utf-8 -*-
# @Time : 2020/10/24
# @Author : Benny Jane
# @Email : 暂无
# @File : __init__.py.py
# @Project : order-backend-web
import base64
import hashlib
import random
import string

ENCODE_MODE_UTF8 = 'utf-8'


class UserService(object):
    @staticmethod
    def geneAuthCode(user_info=None):
        m = hashlib.md5()
        str = "%s-%s-%s-%s" % (user_info.uid, user_info.login_name, user_info.login_pwd, user_info.login_salt)
        m.update(str.encode(ENCODE_MODE_UTF8))
        return m.hexdigest()

    @staticmethod
    def genePwd(pwd, salt):
        m = hashlib.md5()
        str = "{}-{}".format(base64.encodebytes(pwd.encode(ENCODE_MODE_UTF8)), salt)
        m.update(str.encode(ENCODE_MODE_UTF8))
        return m.hexdigest()

    @staticmethod
    def geneSalt(length=16):
        keylist = [random.choice((string.ascii_letters + string.digits)) for _ in range(length)]
        # return ("".join(keylist)) 返回元组  ==》 直接添加一个逗号就可以了
        return "".join(keylist),
