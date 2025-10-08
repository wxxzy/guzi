# 生产环境配置
import os
from config import Config

class ProductionConfig(Config):
    # 数据库配置 - 使用PostgreSQL（推荐用于生产）
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'postgresql://gushi_user:gushi_password@localhost/gushi_db'
    
    # 安全配置
    SECRET_KEY = os.environ.get('SECRET_KEY') or \
        os.urandom(24)  # 在生产环境中应设置为环境变量
    
    # 会话安全
    SESSION_COOKIE_SECURE = True  # 在HTTPS环境下启用
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    
    # CSRF保护
    WTF_CSRF_ENABLED = True
    
    # API限制
    API_RATE_LIMIT = os.environ.get('API_RATE_LIMIT') or '100 per minute'
    
    # 日志配置
    LOG_LEVEL = os.environ.get('LOG_LEVEL') or 'INFO'
    
    # Redis配置（用于缓存和会话）
    REDIS_URL = os.environ.get('REDIS_URL') or 'redis://localhost:6379/0'
    
    # 其他生产环境特定配置
    DEBUG = False
    TESTING = False


class DevelopmentConfig(Config):
    # 开发环境配置
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
        'sqlite:///dev_gushi.db'
    SESSION_COOKIE_SECURE = False  # 开发环境下可禁用


class TestingConfig(Config):
    # 测试环境配置
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    WTF_CSRF_ENABLED = False