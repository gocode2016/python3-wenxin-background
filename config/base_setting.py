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
    'appid': "wx312e4f853deb8168",
    'appsecret': "62a51fb2c7d68cd22460d00dc3fef46d"
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
