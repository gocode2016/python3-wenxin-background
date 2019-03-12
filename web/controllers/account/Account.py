from flask import Blueprint, render_template, request, redirect, jsonify
from common.libs.Helper import ops_templates, iPagination, getCurrentTime
from common.libs.User.UserService import UserService
from common.models.User import User
from common.libs.UrlManager import UrlManager
from sqlalchemy import or_
from application import app, db
import application

account_bp = Blueprint('account', __name__)


class Tmp(object):
    finance = 'hello'
    order = 'wprld'
    member = '1'
    shared = '2'


@account_bp.route('/index')
def index():
    ret_data = {}
    user_info = User.query
    page_info = request.values
    page = int(page_info['p']) if ('p' in page_info and page_info['p']) else 1

    # 查询
    if 'mix_kw' in page_info:
        rule = or_(User.nickname.ilike("%{0}%".format(page_info['mix_kw'])),
                   User.mobile.ilike("%{0}%".format(page_info['mix_kw'])))
        user_info = user_info.filter(rule)

    # 状态判断
    if 'status' in page_info and int(page_info['status']) > -1:
        user_info = user_info.filter(User.status == int(page_info['status']))

    # 分页信息
    page_params = {
        'total': user_info.count(),
        'page_size': app.config['PAGE_SIZE'],
        'page': page,
        'display': app.config["PAGE_DISPLAY"],
        'url': request.full_path.replace("&p={}".format(page), "")
    }

    # 每页显示数据
    offset = (page - 1) * app.config['PAGE_SIZE']
    limit = app.config['PAGE_SIZE'] * page
    all_user_info = user_info.order_by(User.uid.asc()).all()[offset: limit]
    ret_data['list'] = all_user_info

    # 分页处理
    pages = iPagination(page_params)

    ret_data['status_mapping'] = app.config["USER_STATUS"]
    ret_data['pages'] = pages
    ret_data['search_con'] = page_info
    return ops_templates('account/index.html', ret_data)


@account_bp.route('/set', methods=['POST', 'GET'])
def set():
    if request.method == 'GET':
        ret_data = {}
        info = None
        set_info = request.args
        uid = set_info.get('id', 0)
        if uid:
            info = User.query.filter_by(uid=uid).first()
        ret_data['info'] = info
        return ops_templates('account/set.html', ret_data)

    success_info = {'code': 200, 'msg': '添加成功'}
    add_info = request.values
    uid = add_info['id'] if 'id' in add_info else 0
    nickname = add_info['nickname'] if 'nickname' in add_info else None
    mobile = add_info['mobile'] if 'mobile' in add_info else None
    email = add_info['email'] if 'email' in add_info else None
    login_name = add_info['login_name'] if 'login_name' in add_info else None
    login_pwd = add_info['login_pwd'] if 'login_pwd' in add_info else None

    if nickname is None or mobile is None or email is None:
        success_info['msg'] = '用户名、手机号或邮箱输入错误'
        return jsonify(success_info)

    user_info = User.query.filter(User.login_name == login_name).first()
    if login_name is None or user_info:
        success_info['code'] = -1
        success_info['msg'] = '用户名为空或重复'
        return jsonify(success_info)

    # 如果uid存在，进行修改操作；否则进行添加操作
    uid_info = User.query.filter_by(uid=uid).first()
    if uid_info:
        submit_info = uid_info
    else:
        submit_info = User()
        submit_info.created_time = getCurrentTime()
        submit_info.login_salt = UserService.genpwdsalt()

    # 如果uid为1，则不允许进行操作
    if uid == '1':
        success_info['msg'] = '超级管理员账户，无权删除或修改'
        return jsonify(success_info)

    # 信息校验完成，进行提交或修改
    submit_info.nickname = nickname
    submit_info.login_name = login_name
    submit_info.mobile = mobile
    submit_info.email = email
    submit_info.login_pwd = UserService.genpwd(login_pwd, submit_info.login_salt)
    submit_info.updated_time = getCurrentTime()
    db.session.add(submit_info)
    db.session.commit()
    return jsonify(success_info)


@account_bp.route('/info')
def info():
    ret_data = {}
    query_info = request.args
    uid = int(query_info.get('id', 0))
    if uid < 0:
        return redirect(UrlManager.buildUrl('/account/index'))

    user_info = User.query.filter_by(uid=uid).first()
    if not user_info:
        return redirect(UrlManager.buildUrl('/account/index'))
    ret_data['info'] = user_info
    return ops_templates('account/info.html', ret_data)


@account_bp.route("/ops", methods=["POST"])
def ops():
    resp = {'code': 200, 'msg': '操作成功', 'data': {}}
    req = request.values

    id = req['id'] if 'id' in req else 0
    act = req['act'] if 'act' in req else ''
    if not id:
        resp['code'] = -1
        resp['msg'] = "请选择要操作的账号"
        return jsonify(resp)

    if act not in ['remove', 'recover']:
        resp['code'] = -1
        resp['msg'] = "操作有误，请重试"
        return jsonify(resp)

    user_info = User.query.filter_by(uid=id).first()
    if not user_info:
        resp['code'] = -1
        resp['msg'] = "指定账号不存在"
        return jsonify(resp)

    if act == "remove":
        user_info.status = 0
    elif act == "recover":
        user_info.status = 1

    if user_info and user_info.uid == 1:
        resp['code'] = -1
        resp['msg'] = "超级管理员账户，无权删除或修改"
        return jsonify(resp)

    user_info.update_time = getCurrentTime()
    db.session.add(user_info)
    db.session.commit()
    return jsonify(resp)
