from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_script import Manager
import os  # 可以添加环境变量进行配置
from common.libs.UrlManager import UrlManager


class Application(Flask):
    def __init__(self, import_name, template_folder, root_path):
        super(Application, self).__init__(import_name, template_folder=template_folder, root_path=root_path, static_folder=None)
        self.config.from_pyfile('config/base_setting.py')
        self.config.from_pyfile('config/local_setting.py')
        db.init_app(self)

db = SQLAlchemy()
app = Application(__name__, template_folder=os.getcwd() + '/web/templates', root_path=os.getcwd())
manager = Manager(app)

app.add_template_global(UrlManager.buildStaticUrl, 'buildStaticUrl')
app.add_template_global(UrlManager.buildUrl, 'buildUrl')