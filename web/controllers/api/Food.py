from flask import Blueprint, jsonify, request, g
from common.models.food.FoodCat import FoodCat
from common.models.food.Food import Food
from . import api_bp
from common.libs.UrlManager import UrlManager
from sqlalchemy import or_
from common.models.member.MemberCart import MemberCart

@api_bp.route('/food/index', methods=['POST', 'GET'])
def index():
    ret_data = {'code': 200, 'msg': '调用成功', 'data': {}}

    food_cat = FoodCat.query.filter_by(status=1).all()

    food_cat_list = []
    food_cat_list.append({
        'id': 0,
        'name': "全部"
    })
    if food_cat:
        for item in food_cat:
            item_data = {
                'id': item.id,
                'name': item.name
            }
            food_cat_list.append(item_data)

    ret_data['data']['cat_list'] = food_cat_list

    food_list_data = Food.query.all()
    food_list = []
    if food_cat_list:
        for item in food_list_data:
            item_data = {
                'id': item.id,
                'pic_url': UrlManager.buildImageUrl(item.main_image)
            }
            food_list.append(item_data)
    ret_data['data']['banner_list'] = food_list
    return jsonify(ret_data)


@api_bp.route('/food/search', methods=['POST', 'GET'])
def search():
    ret_data = {'code': 200, 'msg': '调用成功', 'data': {}}
    search_info = request.values
    cat_id = search_info['cat_id'] if 'cat_id' in search_info else 0
    mix_kw = search_info['mix_kw'] if 'mix_kw' in search_info else None

    query = Food.query.filter_by(status=1)
    if int(cat_id) > 0:
        query = query.filter(Food.cat_id == cat_id)

    if mix_kw is not None:
        rule = or_(Food.name.ilike('%{0}%'.format(mix_kw)))
        query = query.filter(rule)

    food_list_data = query.all()
    food_list = []
    if food_list_data:
        for item in food_list_data:
            item_data = {
                'id': item.id,
                'name': item.name,
                'price': str(item.price),
                'min_price': str(item.price),
                'pic_url': UrlManager.buildImageUrl(item.main_image)
            }
            food_list.append(item_data)
    ret_data['data']['food_list'] = food_list
    return jsonify(ret_data)


@api_bp.route('/food/info', methods=['POST', 'GET'])
def food_info():
    ret_data = {'code': 200, 'msg': '调用成功', 'data': {}}
    detail_info = request.values
    id = detail_info['id'] if 'id' in detail_info else 0

    info = Food.query.filter_by(id=id).first()
    if info is not None:
        detail_list = {
            'id': id,
            'name': info.name,
            'summary': info.summary,
            "total_count": info.total_count,
            "comment_count": info.comment_count,
            "stock": info.stock,
            "price": str(info.price),
            "main_image": "http://127.0.0.1:9999/static/upload/aa.png",
            "pics": ['http://127.0.0.1:9999/static/upload/bb.jpg']
        }
        ret_data['data']['food_info'] = detail_list

    member_info = g.member_info
    if member_info:
        cart_num = MemberCart.query.filter_by(member_id=member_info.id).count()
    ret_data['data']['cart_num'] = cart_num
    return jsonify(ret_data)
