# 服务端口
SERVER_PORT = 9999

# cookie值，建议进行base转换
COOKIE_NAME = 'fovegage'

# 分页设置
PAGE_SIZE = 2
PAGE_DISPLAY = 10

# 过滤url
IGNORE_URLS = [
    "^/user/login",
    "^/static",
    "^/favicon.ico",
    "^/api"
]

# 用户状态
USER_STATUS = {
    '1': '正常',
    '0': "已删除"
}

# 微信key
MINA = {
    'appid': "wxa5085ab44202abbd",
    'appsecret': "d0d28f24b687f1b961bb76336dc623fa"
}

STATUS_MAPPING = {
    '1': '正常',
    '0': '禁用'
}

UPLOAD = {
    'ext': ['jpg', 'gif', 'bmp', 'jpeg', 'png'],
    'prefix_path': '/web/static/upload/',
    'prefix_url': '/static/upload/aa.png'
}

APP = {
    'domain': 'http://127.0.0.1:9999'
}

PAY_STATUS_DISPLAY_MAPPING = {
    '-8': '待支付'
}

MERCH_INFO = {
    "appid": "wxa5085ab44202abbd",
    "mch_id": "1526080001",
    'key': "6jcv4yqiREX22SodocIto2H0KQbzBlr0"
}
