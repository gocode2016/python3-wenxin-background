from flask import Blueprint

api_bp = Blueprint('api_bp', __name__)
from .Member import *
from .Food import  *
from .Cart import *
from .Order import *

@api_bp.route('/')
def api():
    return 'Api V1'
