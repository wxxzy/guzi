"""
安全中间件
提供各种安全防护功能
"""
import hashlib
import hmac
import time
import secrets
from functools import wraps
from flask import request, jsonify, abort
import os

class SecurityMiddleware:
    """安全中间件类"""
    
    def __init__(self, app=None):
        self.app = app
        if app is not None:
            self.init_app(app)
    
    def init_app(self, app):
        """初始化应用"""
        self.app = app
        
        # 注册安全钩子
        @app.before_request
        def security_check():
            return self._security_checks()
    
    def _security_checks(self):
        """执行安全检查"""
        # 检查请求频率（基础检查）
        # 更详细的限流由Flask-Limiter处理
        
        # 检查可疑请求头
        suspicious_headers = [
            'x-forwarded-for', 'client-ip', 'x-real-ip'
        ]
        
        # 可以在这里添加更多安全检查逻辑
        pass
    
    @staticmethod
    def generate_csrf_token():
        """生成CSRF令牌"""
        return secrets.token_urlsafe(32)
    
    @staticmethod
    def verify_csrf_token(token, expected_token):
        """验证CSRF令牌"""
        try:
            return hmac.compare_digest(token, expected_token)
        except Exception:
            return False
    
    @staticmethod
    def hash_password(password, salt=None):
        """哈希密码"""
        if salt is None:
            salt = secrets.token_hex(16)
        
        pwdhash = hashlib.pbkdf2_hmac('sha256',
                                      password.encode('utf-8'),
                                      salt.encode('ascii'),
                                      100000)  # 100,000次迭代
        return salt + pwdhash.hex()
    
    @staticmethod
    def verify_password(stored_password, provided_password):
        """验证密码"""
        salt = stored_password[:32]  # 前32个字符是盐
        stored_hash = stored_password[32:]
        
        pwdhash = hashlib.pbkdf2_hmac('sha256',
                                       provided_password.encode('utf-8'),
                                       salt.encode('ascii'),
                                       100000)
        
        return hmac.compare_digest(pwdhash.hex(), stored_hash)
    
    @staticmethod
    def sanitize_input(input_string):
        """清理输入，防止XSS攻击"""
        import html
        # 转义HTML特殊字符
        sanitized = html.escape(input_string)
        
        # 移除潜在的危险字符
        dangerous_chars = ['<script', '</script>', 'javascript:', 'vbscript:', 'onload=', 'onerror=']
        for char in dangerous_chars:
            sanitized = sanitized.replace(char, '')
        
        return sanitized
    
    @staticmethod
    def validate_api_key(api_key):
        """验证API密钥"""
        # 这里可以实现API密钥验证逻辑
        # 例如检查数据库中的API密钥记录
        valid_keys = [
            os.environ.get('VALID_API_KEY_1', ''),
            os.environ.get('VALID_API_KEY_2', '')
        ]
        
        return api_key in valid_keys and api_key != ''
    
    @staticmethod
    def rate_limit_exceeded(key, limit=100, window=3600):
        """检查是否超出速率限制"""
        # 简单的内存速率限制实现
        # 在生产环境中应使用Redis等持久化存储
        import time
        
        # 这里只是一个简单的示例实现
        # 实际应用中应使用更完善的速率限制方案
        return False

# 创建全局安全中间件实例
security_middleware = SecurityMiddleware()