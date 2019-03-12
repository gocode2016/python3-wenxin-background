from . import api_bp
from flask import jsonify, request, g
import json, decimal
from common.models.food.Food import Food
from common.libs.Order.OrderService import OrderService

@api_bp.route('/order/info', methods=["POST", 'GET'])
def order_info():
    ret_data = {'code': 200, 'msg': '调用成功', 'data': {}}
    order_info = request.values
    order_type = order_info['type'] if 'type' in order_info else None
    goods = order_info['goods'] if 'goods' in order_info else None

    if order_type is None or goods is None:
        ret_data['code'] = -1
        ret_data['msg'] = '失败'
        return jsonify(ret_data)

    food_dic = {}
    for item in json.loads(goods):
        food_dic[item['id']] = item['number']

    food_list = Food.query.filter(Food.id.in_(food_dic.keys())).all()

    food_lists = []
    if food_list:
        pay_price = 0
        for item in food_list:
            per_info = {
                'id': item.id,
                'price': str(item.price),
                'name': item.name,
                'pic_url': item.main_image,
                'number': food_dic[item.id]
            }
            food_lists.append(per_info)
            yun_price = decimal.Decimal('0.00')
            pay_price = pay_price + item.price * food_dic[item.id]

    ret_data['data']['food_list'] = food_lists
    ret_data['data']['yun_price'] = str(yun_price)
    ret_data['data']['shop_price'] = str(pay_price)
    ret_data['data']['total_price'] = str(pay_price + yun_price)
    return jsonify(ret_data)

@api_bp.route('/order/create', methods=["POST", 'GET'])
def order_create():
    ret_data = {'code': 200, 'msg': '调用成功', 'data': {}}
    order_info = request.values
    type_info = order_info['type'] if 'type' in order_info else None
    cart_info = order_info['goods'] if 'goods' in order_info else None

    item = []
    params = {}  # 额外参数
    if type_info and cart_info:
        item = json.loads(cart_info)
    member_info = g.member_info
    OrderService().PayService(member_info.id, item, params)
    return jsonify(ret_data)
