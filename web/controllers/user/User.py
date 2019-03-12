from flask import Blueprint, render_template, request, jsonify, make_response, redirect, g
from common.models.User import User
from common.libs.User.UserService import UserService
import application
from common.libs.UrlManager import UrlManager
from common.libs.Helper import ops_templates
from common.libs.User.UserService import UserService

user_bp = Blueprint('login', __name__)


class Tmp(object):
    finance = 'hello'
    order = 'wprld'
    member = '1'
    shared = '2'


@user_bp.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == "GET":
        return render_template('user/login.html')
    info = {'code': 200, 'msg': "登录成功", 'data': {}}
    login_info = request.values
    username = login_info['login_name'] if 'login_name' in login_info else ''
    password = login_info['login_pwd'] if 'login_pwd' in login_info else ''

    if (username or password) is None or len(username) < 1:
        info['code'] = 201
        info['msg'] = '请输入正确的用户名或密码'
        return jsonify(info)

    user_info = User.query.filter_by(login_name=username).first()
    if not user_info:
        info['code'] = 202
        info['msg'] = '用户名或密码错误'
        return jsonify(info)

    if user_info.login_pwd != UserService.genpwd(password, user_info.login_salt):
        info['code'] = 203
        info['msg'] = '用户名或密码错误'
        return jsonify(info)

    response = make_response(jsonify(info))
    response.set_cookie(application.app.config['COOKIE_NAME'],
                        "{}#{}".format(UserService.cookieAuth(user_info), user_info.uid))
    return response


@user_bp.route('/edit', methods=['POST', 'GET'])
def edit():
    if request.method == "GET":
        return ops_templates('user/edit.html', {'current':'edit'})
    info = {'code': 200, 'msg': "修改成功", 'data': {}}

    modify_info = request.values

    nickname = modify_info['nickname'] if 'nickname' in modify_info else None
    email = modify_info['email'] if 'email' in modify_info else None

    user_info = g.current_user
    user_info.nickname = nickname
    user_info.email = email

    application.db.session.add(user_info)
    application.db.session.commit()
    return jsonify(info)


@user_bp.route('/reset-pwd', methods=['POST', 'GET'])
def reset():
    if request.method == "GET":
        return ops_templates('user/reset_pwd.html', {'current':'reset-pwd'})
    info = {'code': 200, 'msg': "密码修改成功", 'data': {}}

    reset_info = request.values
    old_password = reset_info['old_password'] if 'old_password' in reset_info else None
    new_password = reset_info['new_password'] if 'new_password' in reset_info else None

    if old_password == new_password:
        info['msg'] = '两次输入密码一致，请重新输入'
        info['code'] = -2
        return jsonify(info)
    user_info = g.current_user
    user_info.login_pwd = UserService.genpwd(new_password, user_info.login_salt)
    application.db.session.add(user_info)
    application.db.session.commit()
    return jsonify(info)


@user_bp.route('/logout')
def logout():
    response = make_response(redirect(UrlManager.buildUrl('/user/login')))
    response.delete_cookie(application.app.config['COOKIE_NAME'])
    return response
