import os
import atexit
from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from config import DevelopmentConfig, ProductionConfig, TestingConfig
from models import db
from security.config import SecurityConfig

# 导入监控组件
from monitoring import initialize_monitoring_system, start_monitoring_services, stop_monitoring_services
from monitoring.api import monitoring_bp

def create_app(config_name=None):
    app = Flask(__name__)
    
    # 根据环境变量设置配置
    if config_name is None:
        config_name = os.environ.get('FLASK_ENV', 'development')
    
    if config_name == 'production':
        app.config.from_object(ProductionConfig)
    elif config_name == 'testing':
        app.config.from_object(TestingConfig)
    else:
        app.config.from_object(DevelopmentConfig)
    
    # 初始化数据库
    db.init_app(app)
    
    # 初始化监控系统
    initialize_monitoring_system()
    
    # 设置API限流
    limiter = Limiter(
        key_func=get_remote_address,
        default_limits=[SecurityConfig.API_RATE_LIMIT]  # 使用安全配置的默认限制
    )
    limiter.init_app(app)
    
    # Enable CORS - 生产环境中应限制来源
    if app.config['DEBUG']:
        CORS(app, origins=["http://localhost:3000", "http://localhost:5000", "*"])  # 开发环境允许所有来源
    else:
        # 生产环境中限制CORS来源
        CORS(app, resources={
            r"/api/*": {"origins": os.environ.get('FRONTEND_URL', 'http://localhost:3000')}
        })
    
    # 添加安全头和CSP
    @app.after_request
    def after_request(response):
        """添加安全头和CSP到每个响应"""
        # 添加安全头
        for header, value in SecurityConfig.SECURITY_HEADERS.items():
            response.headers[header] = value
        
        # 添加内容安全策略
        response.headers['Content-Security-Policy'] = SecurityConfig.get_csp_string()
        
        return response
    
    # 请求预处理
    @app.before_request
    def before_request():
        """请求预处理"""
        # 限制请求大小
        if request.content_length and request.content_length > SecurityConfig.MAX_CONTENT_LENGTH:
            return jsonify({'error': '请求体过大'}), 413
        
        # 可以在这里添加更多的安全检查
    
    # 应用启动后处理
    with app.app_context():
        # 启动监控服务
        start_monitoring_services()
    
    # 应用关闭前处理
    @app.teardown_appcontext
    def shutdown(exception=None):
        """应用关闭前执行"""
        pass
    
    # 错误处理器
    @app.errorhandler(429)
    def ratelimit_handler(e):
        """处理速率限制错误"""
        return jsonify({
            'error': '请求过于频繁',
            'message': '请稍后再试'
        }), 429
    
    @app.errorhandler(404)
    def not_found(error):
        """处理404错误"""
        return jsonify({'error': '资源未找到'}), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        """处理500错误"""
        db.session.rollback()
        return jsonify({'error': '服务器内部错误'}), 500
    
    # 注册蓝图
    from routes.main import main_bp
    from routes.stock import stock_bp
    from routes.analysis import analysis_bp
    
    app.register_blueprint(main_bp)
    app.register_blueprint(stock_bp)
    app.register_blueprint(analysis_bp)
    app.register_blueprint(monitoring_bp)  # 注册监控蓝图
    
    return app

# 注册应用退出处理函数
atexit.register(stop_monitoring_services)

if __name__ == '__main__':
    app = create_app()
    with app.app_context():
        db.create_all()
    app.run(debug=True)