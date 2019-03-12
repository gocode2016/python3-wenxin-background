from flask import Blueprint
from common.libs.Helper import ops_templates


member_bp = Blueprint('member_bp', __name__)

@member_bp.route('/index')
def index():
    ret_data = {}
    ret_data['search_con'] = None
    ret_data['pages'] = None
    return ops_templates('/member/index.html', ret_data)