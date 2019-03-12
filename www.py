from web.controllers.index import index_bp
from application import app
from web.controllers.user.User import user_bp
from web.controllers.static import static_bp
from web.controllers.account.Account import account_bp
from web.Interceptor.CookieAuth import *
from web.controllers.api import api_bp
from web.controllers.food.food import food_bp
from web.controllers.member.member import member_bp
# from web.controllers.uploads.upload import route_upload

app.register_blueprint(index_bp, url_prefix='/')
app.register_blueprint(user_bp, url_prefix='/user')
app.register_blueprint(static_bp, url_prefix='/static')
app.register_blueprint(account_bp, url_prefix='/account')
app.register_blueprint(food_bp, url_prefix='/food')
app.register_blueprint(member_bp, url_prefix='/member')
app.register_blueprint(api_bp, url_prefix='/api')
# app.register_blueprint(route_upload, url_prefix='/upload')