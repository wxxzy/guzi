# guzi_backend/__init__.py

from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from .config import config
from .database import db
from .services.ai_manager import ai_manager

# 初始化JWTManager
jwt = JWTManager()

def create_app(config_name='default'):
    """创建并配置Flask应用实例（应用工厂模式）。"""
    app = Flask(__name__)

    # 初始化CORS，允许所有来源进行跨域请求（开发环境）
    CORS(app)

    # 从配置对象中加载配置
    app.config.from_object(config[config_name])

    # 初始化JWT
    jwt.init_app(app)

    # 初始化SQLAlchemy
    db.init_app(app)

    # 初始化AI管理器
    ai_manager.init_app(app)
    app.ai_manager = ai_manager # 将ai_manager挂载到app对象上，方便访问

    # 注册蓝图
    from .routes.main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .routes.auth import auth_bp
    app.register_blueprint(auth_bp)

    from .routes.watchlist import watchlist_bp
    app.register_blueprint(watchlist_bp)

    return app
