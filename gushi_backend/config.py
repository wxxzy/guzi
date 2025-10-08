import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard-to-guess-string'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # AI服务配置
    QWEN_API_KEY = os.environ.get('QWEN_API_KEY')
    QWEN_BASE_URL = os.environ.get('QWEN_BASE_URL', 'https://dashscope.aliyuncs.com/compatible-mode/v1')
    
    # OpenAI API密钥（用于兼容API）
    OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')
    
    # 火山引擎API配置（使用OpenAI SDK方式）
    VOLC_API_KEY = os.environ.get('VOLC_API_KEY')
    VOLC_REGION = os.environ.get('VOLC_REGION', 'cn-beijing')
    VOLC_MODEL_NAME = os.environ.get('VOLC_MODEL_NAME', 'doubao-pro-128k')  # 默认模型
    VOLC_BASE_URL = os.environ.get('VOLC_BASE_URL', 'https://ark.cn-beijing.volces.com/api/v3')  # 火山引擎OpenAI兼容API地址
    
    # 数据源配置
    AKSHARE_TOKEN = os.environ.get('AKSHARE_TOKEN')


class DevelopmentConfig(Config):
    # 开发环境配置
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or 'sqlite:///dev_gushi.db'


class ProductionConfig(Config):
    # 生产环境配置
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///gushi_prod.db'
    DEBUG = False


class TestingConfig(Config):
    # 测试环境配置
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    WTF_CSRF_ENABLED = False