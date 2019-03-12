import application
from flask import request, redirect, g
from common.models.User import User
from common.models.member.Member import Member
from common.libs.User import UserService
from common.libs.Member import MemberService
from common.libs.UrlManager import UrlManager
import re


@application.app.before_request
def before_request():
    ignore_urls = application.app.config['IGNORE_URLS']
    path = request.path
    pattern = re.compile('%s' % "|".join(ignore_urls))

    if path.startswith('/api'):
        member_info = check_wx_login()
        g.member_info = member_info

    if pattern.match(path):
        return

    user_info = ckeck_login()
    g.current_user = None
    if user_info:
        g.current_user = user_info

    if not user_info:
        return redirect(UrlManager.buildUrl('/user/login'))


"""
判断是否登录
"""


def ckeck_login():
    cookie = request.cookies
    auth_cookie = cookie[application.app.config['COOKIE_NAME']] if application.app.config[
                                                                       'COOKIE_NAME'] in cookie else None

    if auth_cookie is None:
        return False

    auth_info = auth_cookie.split("#")
    if len(auth_info) != 2:
        return False
    user_info = User.query.filter_by(uid=auth_info[1]).first()

    if user_info is None:
        return False

    if auth_info[0] != UserService.UserService.cookieAuth(user_info):
        return False

    return user_info


def check_wx_login():
    token = request.headers.get("Authorization")
    if token is None:
        return False

    auth_info = str(token).split('#')
    if len(auth_info) != 2:
        return False

    member_info = Member.query.filter_by(id=auth_info[1]).first()
    if member_info is None:
        return False

    if auth_info[0] != MemberService.MemberService.geneAuthCode(member_info):
        return False

    return member_info
