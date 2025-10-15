# guzi_backend/__init__.py

from flask import Flask

def create_app():
    """创建并配置Flask应用实例（应用工厂模式）。"""
    app = Flask(__name__)

    # 在这里可以加载配置，例如从一个config.py文件
    # app.config.from_object('guzi_backend.config.DevelopmentConfig')

    # 注册蓝图
    from .routes.main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    # 可以在这里初始化扩展，例如数据库
    # from .models import db
    # db.init_app(app)

    return app
