from flask import request, jsonify, g
from . import api_bp
from application import app, db
import requests
import json
from common.models.member.Member import Member
from common.models.member.OauthMemberBind import OauthMemberBind
from common.libs.Helper import getCurrentTime
from common.libs.User.UserService import UserService
from common.libs.Member.MemberService import MemberService


# 用户身份识别
@api_bp.route('/wx/login', methods=["POST", "GET"])
def wx_login():
    success_info = {'code': 200, "msg": "成功", 'data': {}}
    login_info = request.values
    code = login_info['code'] if 'code' in login_info else None
    if code is None:
        success_info['code'] = -1
        success_info['msg'] = '为产生code'
    url = "https://api.weixin.qq.com/sns/jscode2session?appid={0}&secret={1}&js_code={2}&grant_type=authorization_code".format(
        app.config['MINA']['appid'], app.config['MINA']['appsecret'], code)

    ret_data = requests.get(url)
    openid = json.loads(ret_data.text)['openid']

    nickName = login_info['nickName'] if 'nickName' in login_info else None
    sex = login_info['sex'] if 'sex' in login_info else None
    avatarUrl = login_info['avatarUrl'] if 'avatarUrl' in login_info else None
    # 如果绑定直接返回用户信息
    mind_info = OauthMemberBind.query.filter_by(openid=openid, type=1).first()
    if not mind_info:
        # 插入会员信息
        member = Member()
        member.nickname = nickName
        member.sex = sex
        member.avatar = avatarUrl
        member.salt = UserService.genpwdsalt()
        member.updated_time = member.created_time = getCurrentTime()
        db.session.add(member)
        db.session.commit()

        # 绑定会员信息
        mind = OauthMemberBind()
        mind.member_id = member.id
        mind.type = 1
        mind.openid = openid
        mind.extra = ''
        mind.updated_time = mind.created_time = getCurrentTime()
        db.session.add(mind)
        db.session.commit()

        mind_info = mind

    member_info = Member.query.filter_by(id=mind_info.member_id).first()
    token = "{0}#{1}".format(MemberService.geneAuthCode(member_info), mind_info.id)
    success_info['data'] = token
    return jsonify(success_info)


# 用户注册检测
@api_bp.route('/wx/check', methods=["POST", 'GET'])
def check():
    success_info = {'code': 201, 'msg': '成功'}
    check_login = request.values
    code = check_login['code'] if 'code' in check_login else None
    if code is None:
        success_info['code'] = -1
        success_info['msg'] = "失败"
        return jsonify(success_info)
    print(code)
    return jsonify(success_info)


# 返回用户信息
@api_bp.route('/member/info', methods=["POST", 'GET'])
def info():
    success_info = {'code': 200, 'msg': '成功', 'data': {}}
    member_info = g.member_info
    if member_info:
        success_info['data']['info'] = {
            "nickname": member_info.nickname,
            "avatar_url": member_info.avatar
        }
    else:
        success_info['code'] = -1
        success_info['msg'] = '鉴权失败'
    return jsonify(success_info)
