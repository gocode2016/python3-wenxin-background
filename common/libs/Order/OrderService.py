from common.models.pay.PayOrder import PayOrder
from common.models.pay.PayOrderCallbackData import PayOrderCallbackData
from common.models.pay.PayOrderItem import PayOrderItem
import decimal


class OrderService(object):

    def PayService(self, member_id, order_info, params):
        # 遍历商品信息
        pay_price = decimal.Decimal(0.00)
        foods_id = []
        for item in order_info:
            if decimal.Decimal(item['price']) > 0:
                return 'error'
            pay_price = pay_price + decimal.Decimal(item['price']) * int(item['number'])
            foods_id.append(item['id'])
        yun_price = params['yun_price'] if params and 'yun_price' in params else 0
        note = params['note'] if params and 'note' in params else ''
        express_address_id = params['express_address_id'] if params and 'express_address_id' in params else 0
        express_info = params['express_info'] if params and 'express_info' in params else {}
        yun_price = decimal.Decimal(yun_price)
        total_price = pay_price + yun_price

        try:
            pass

        except Exception as e:
            pass
