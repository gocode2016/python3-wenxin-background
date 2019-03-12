from . import api_bp
from flask import jsonify, request, g
from common.models.member.MemberCart import MemberCart
from common.libs.Food.FoodService import getFoodInfo
from common.libs.Helper import getCurrentTime
from application import db

@api_bp.route('/cart/info', methods=['POST', "GET"])
def cart_info():
    success_info = {'code': 200, "msg": "添加成功", 'data': {}}
    member_info = g.member_info
    cart_info = MemberCart.query.filter_by(member_id=member_info.id).all()

    cart_list = []
    if cart_info:
        for item in cart_info:
            food_info = getFoodInfo(item.food_id)
            per_info = {
                "id": item.id,
                "food_id": item.food_id,
                "pic_url": food_info.main_image,
                "name": food_info.name,
                "price": str(food_info.price),
                "active": True,
                "number": item.quantity
            }
            cart_list.append(per_info)
    success_info['data']['cart_list'] = cart_list
    return jsonify(success_info)


@api_bp.route('/cart/set', methods=['POST'])
def cart_set():
    success_info = {'code': 200, "msg": "添加成功", 'data': {}}
    cart_info = request.values
    id = cart_info['id'] if 'id' in cart_info else None
    num = cart_info['num'] if 'num' in cart_info else None

    member_id = g.member_info.id
    if id is None or num is None:
        success_info['code'] = -1
        success_info['msg'] = 'error'
    is_food = MemberCart.query.filter_by(food_id=id).first()

    if is_food:
        is_food.quantity = int(num)
        is_food.updated_time = getCurrentTime()
        db.session.add(is_food)
        db.session.commit()

    else:
        membercart = MemberCart()
        membercart.member_id = member_id
        membercart.food_id = id
        membercart.quantity = num
        membercart.updated_time = membercart.created_time = getCurrentTime()
        db.session.add(membercart)
        db.session.commit()

    return jsonify(success_info)
