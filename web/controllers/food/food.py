from flask import Blueprint, request, jsonify
from common.libs.Helper import ops_templates
from common.models.food.Food import Food
from common.models.food.FoodCat import FoodCat
from common.libs.Helper import getCurrentTime
from application import db, app

food_bp = Blueprint('food_bp', __name__)


@food_bp.route('/index')
def index():
    ret_data = {}
    search_con = ''
    pages = ""
    list = Food.query.all()
    food_cat = FoodCat.query.all()
    ret_data['search_con'] = search_con
    ret_data['pages'] = pages
    ret_data['current'] = 'index'
    ret_data['list'] = list
    ret_data['cat_mapping'] = {1: food_cat,}
    return ops_templates('/food/index.html', ret_data)


@food_bp.route('/set', methods=['POST', 'GET'])
def set():
    if request.method == 'GET':
        ret_data = {}
        search_con = ''
        pages = ""
        info = ''
        cat_info = FoodCat.query.all()
        ret_data['search_con'] = search_con
        ret_data['pages'] = pages
        ret_data['info'] = info
        ret_data['cat_list'] = cat_info
        return ops_templates('/food/set.html', ret_data)
    success_info = {'code': 200, 'msg': '添加分类成功'}
    get_info = request.values
    cat_id = get_info['cat_id'] if 'cat_id' in get_info else None
    name = get_info['name'] if 'name' in get_info else None
    price = get_info['price'] if 'price' in get_info else None
    pic = get_info['main_image'] if 'main_image' in get_info else None
    summary = get_info['summary'] if 'summary' in get_info else None
    stock = get_info['stock'] if 'stock' in get_info else None
    tags = get_info['tags'] if 'tags' in get_info else None

    food_info = Food()
    food_info.name = name
    food_info.cat_id = cat_id
    food_info.price = price
    food_info.main_image = pic
    food_info.summary = summary
    food_info.stock = stock
    food_info.tags = tags
    db.session.add(food_info)
    db.session.commit()
    return jsonify(success_info)


@food_bp.route('/cat', methods=['POST', 'GET'])
def cat():
    if request.method == "GET":
        get_info = request.values
        ret_data = {}
        query = FoodCat.query
        if 'status' in get_info and int(get_info['status']) > -1:
            query = query.filter(FoodCat.status == int(get_info['status']))

        cat_info = query.all()
        ret_data['list'] = cat_info
        ret_data['search_con'] = get_info
        ret_data['current'] = 'cat'
        ret_data['status_mapping'] = app.config['STATUS_MAPPING']
        return ops_templates('/food/cat.html', ret_data)


@food_bp.route('/cat-set', methods=["POST", 'GET'])
def cat_set():
    if request.method == "GET":
        ret_data = {}
        cat_info = None
        get_id = request.args
        id = get_id.get('id', 0)
        if id:
            cat_info = FoodCat.query.filter_by(id=id).first()
        ret_data['info'] = cat_info
        ret_data['current'] = 'cat'
        return ops_templates('/food/cat_set.html', ret_data)

    success_info = {'code': 200, 'msg': '添加分类成功'}
    cat_info = request.values

    id = cat_info['id'] if 'id' in cat_info else 0
    name = cat_info['name'] if 'name' in cat_info else None
    weight = cat_info['weight'] if 'weight' in cat_info else None

    if name is None or weight is None:
        success_info['code'] = -1
        success_info['msg'] = '错误'
        return jsonify(success_info)

    if id:
        cat_info = FoodCat.query.filter_by(id=id).first()

    else:
        cat_info = FoodCat()
        cat_info.created_time = getCurrentTime()

    cat_info.name = name
    cat_info.weight = weight
    cat_info.updated_time = getCurrentTime()
    db.session.add(cat_info)
    db.session.commit()
    return jsonify(success_info)


@food_bp.route('/cat-ops', methods=['POST', 'GET'])
def modity_status():
    success_info = {'code': 200, 'msg': '操作成功'}
    get_info = request.values
    id = get_info['id'] if 'id' in get_info else None
    act = get_info['act'] if 'act' in get_info else None

    cat_info = FoodCat.query.filter_by(id=id).first()
    if act == 'remove' and cat_info:
        cat_info.status = 0
        cat_info.updated_time = getCurrentTime()

    elif act == 'recover' and cat_info:
        cat_info.status = 1
        cat_info.updated_time = getCurrentTime()

    db.session.add(cat_info)
    db.session.commit()

    return jsonify(success_info)
