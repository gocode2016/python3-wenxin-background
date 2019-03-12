from flask import Blueprint, g
from common.libs import Helper

index_bp = Blueprint('index', __name__)



@index_bp.route('/')
def index():

    return Helper.ops_templates('index/index.html')