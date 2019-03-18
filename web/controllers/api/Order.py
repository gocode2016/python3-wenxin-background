from . import api_bp
from flask import jsonify, request, g
import json, decimal
from common.models.food.Food import Food
from common.libs.Order.OrderService import OrderService, PayService
from common.models.pay.PayOrder import PayOrder
from common.models.pay.PayOrderItem import PayOrderItem
from common.libs.Food.FoodService import getFoodInfo

# 订单信息的预览
@api_bp.route('/order/info', methods=["POST"])
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


# 订单数据插入数据库
@api_bp.route('/order/create', methods=["POST"])
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
    target = OrderService()
    ret_data = target.PayService(member_info.id, item, params)
    return jsonify(ret_data)


# 订单数据展现
@api_bp.route('/order/list', methods=["POST"])
def order_list():
    ret_data = {'code': 200, 'msg': '调用成功', 'data': {}}
    status_info = request.values
    status = int(status_info['status']) if 'status' in status_info else 0
    member_info = g.member_info
    query = PayOrder.query.filter_by(member_id=member_info.id)
    if status == -8:
        query = query.filter(PayOrder.status == -8)
    elif status == -7:
        query = query.filter(PayOrder.status == 1)
    elif status == -6:
        query = query.filter(PayOrder.status == 1)
    elif status == 1:
        query = query.filter(PayOrder.status == 1)
    else:
        query = query.filter(PayOrder.status == 1)

    order_list = query.order_by(PayOrder.id.desc()).all()

    if order_list:
        order_ids = [item.id for item in order_list]
        all_order = PayOrderItem.query.filter(PayOrderItem.pay_order_id.in_(order_ids)).all()
        pay_order_item_map = {}
        if all_order:
            for item in all_order:
                if item.pay_order_id not in pay_order_item_map:
                    pay_order_item_map[item.pay_order_id] = []
                pay_order_item_map[item.pay_order_id].append({
                    'main_pic': getFoodInfo(item.food_id).main_image
                })


        pay_detail = []
        for item in order_list:
            tmp_data = {
                'status': item.pay_status,
                'status_desc': item.status_desc,
                'date': item.created_time.strftime("%Y-%m-%d %H:%M:%S"),
                'order_number': item.order_number,
                'order_sn': item.order_sn,
                'note': item.note,
                'total_price': str(item.total_price),
                'goods_list': pay_order_item_map[item.id]
            }
            pay_detail.append(tmp_data)

    ret_data['data']['order_list'] = pay_detail
    return jsonify(ret_data)

@api_bp.route('/order/pay', methods=["POST"])
def order_pay():
    ret_data = {'code': 200, 'msg': '调用成功', 'data': {}}
    pay = PayService()
    info = pay.create_pay({
        "hello": 1,
        'kk': "www"
    })
    print(info)
    return jsonify(ret_data)
