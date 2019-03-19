from common.models.pay.PayOrder import PayOrder
from common.models.food.Food import Food
from common.models.pay.PayOrderCallbackData import PayOrderCallbackData
from common.models.pay.PayOrderItem import PayOrderItem
import decimal
from application import db
from common.libs.Helper import genOrderNo, getCurrentTime
from application import app
from hashlib import md5
import xml.etree.ElementTree as ET
import requests
from common.libs import genNO
class OrderService(object):

    def __init__(self):
        pass

    def PayService(self, member_id, order_info=None, params=None):
        resp = {'code': 200, 'msg': '操作成功~', 'data': {}}
        # 遍历商品信息
        pay_price = decimal.Decimal(0.00)
        foods_id = []
        for item in order_info:
            if decimal.Decimal(item['price']) < 0:
                return 'error'
            pay_price = pay_price + decimal.Decimal(item['price']) * int(item['number'])
            foods_id.append(item['id'])
        yun_price = params['yun_price'] if params and 'yun_price' in params else 0
        note = params['note'] if params and 'note' in params else ''
        express_address_id = params['express_address_id'] if params and 'express_address_id' in params else 0
        express_info = params['express_info'] if params and 'express_info' in params else ''
        yun_price = decimal.Decimal(yun_price)
        total_price = pay_price + yun_price
        try:
            # 查询商品信息
            tmp_food_list = db.session.query(Food).filter(Food.id.in_(foods_id)).with_for_update().all()

            # {id: stock}形式记录
            tmp_food_stock = {}
            for item in tmp_food_list:
                tmp_food_stock[item.id] = item.stock

            pay_order = PayOrder()
            pay_order.order_sn = genOrderNo()
            pay_order.member_id = member_id
            pay_order.total_price = total_price
            pay_order.yun_price = yun_price
            pay_order.note = note
            pay_order.status = -8
            pay_order.express_status = -8
            pay_order.express_address_id = express_address_id
            pay_order.express_info = express_info
            pay_order.updated_time = pay_order.created_time = getCurrentTime()
            db.session.add(pay_order)

            # 生成订单项 减库存
            for item in order_info:
                tmp_stock = tmp_food_stock[item['id']]  # 临时库存
                if int(item['number']) > int(tmp_stock):
                    raise Exception('库存不足')

                update_stock = Food.query.filter_by(id=item['id']).update({
                    'stock': int(tmp_stock) - int(item['number'])
                })
                if not update_stock:
                    raise Exception('非法操作')

                pay_item = PayOrderItem()
                pay_item.pay_order_id = pay_order.id
                pay_item.member_id = member_id
                pay_item.quantity = item['number']
                pay_item.price = item['price']
                pay_item.food_id = item['id']
                pay_item.note = note
                pay_item.updated_time = pay_item.created_time = getCurrentTime()
                db.session.add(pay_item)
            db.session.commit()

        except Exception as e:
            db.session.rollback()
            resp['code'] = -100000
            resp['msg'] = '数据回滚'
            resp['data'] = {'info': e.args}
            return resp

        return resp


class PayService(object):
    def __init__(self):
        pass

    def create_sign(self, pay_data):
        """
        :param:
        :return: md5()
        """
        stringA = '&'.join(["{}={}".format(item, pay_data.get(item)) for item in sorted(pay_data)])
        stringSignTemp = stringA + "&key={}".format(app.config["MERCH_INFO"]["key"])
        sign = md5(stringSignTemp.encode('utf-8')).hexdigest()
        return sign.upper()

    def send_pay_info(self, pay_info):
        sign = self.create_sign(pay_info)
        pay_info['sign'] = sign
        send_data = self.dict_to_xml(pay_info)
        print(send_data)
        headers = {'Content-Type': 'application/xml'}
        url = "https://api.mch.weixin.qq.com/pay/unifiedorder"
        res = requests.post(url=url, headers=headers, data=send_data)
        print(res.text.encode('ISO-8859-1'))
    def dict_to_xml(self, dict_info):
        xml = ['<xml>']
        for key, value in dict_info.items():
            xml.append("<{1}>{0}</{1}>".format(value, key))
        xml.append('</xml>')
        return ''.join(xml)

    def xml_to_dict(self, xml_info):
        xml_dict = {}
        root = ET.fromstring(xml_info)
        for child in root:
            xml_dict[child.tag] = child.text
        return xml_dict
