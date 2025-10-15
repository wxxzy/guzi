# guzi_backend/__init__.py

from flask import Flask
from .config import config
from .database import db

def create_app(config_name='default'):
    """创建并配置Flask应用实例（应用工厂模式）。"""
    app = Flask(__name__)

    # 从配置对象中加载配置
    app.config.from_object(config[config_name])

    # 初始化SQLAlchemy
    db.init_app(app)

    # 注册蓝图
    from .routes.main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app
