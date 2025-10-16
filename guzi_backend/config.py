# guzi_backend/config.py

import os

# 获取项目根目录
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    """基础配置类"""
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'a-hard-to-guess-string'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class DevelopmentConfig(Config):
    """开发环境配置"""
    # 使用DuckDB作为开发数据库
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
        'duckdb:///' + os.path.join(basedir, '../guzi_dev.db')
    GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY')

class ProductionConfig(Config):
    """生产环境配置"""
    # 生产环境应使用PostgreSQL
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY')

# 导出一个配置字典，方便根据环境变量选择
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}

