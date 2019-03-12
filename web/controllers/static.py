from flask import Blueprint, send_from_directory
import application

static_bp = Blueprint('static', __name__)


@static_bp.route('/<path:name>')
def static(name):
    return send_from_directory(application.app.root_path + '/web/static', name)
