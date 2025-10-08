"""
安全配置
"""
import os

class SecurityConfig:
    """安全配置类"""
    
    # 密码安全
    MIN_PASSWORD_LENGTH = int(os.environ.get('MIN_PASSWORD_LENGTH', '8'))
    MAX_PASSWORD_LENGTH = int(os.environ.get('MAX_PASSWORD_LENGTH', '128'))
    
    # 会话安全
    SESSION_TIMEOUT = int(os.environ.get('SESSION_TIMEOUT', '3600'))  # 1小时
    SESSION_COOKIE_SECURE = os.environ.get('SESSION_COOKIE_SECURE', 'True').lower() == 'true'
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    
    # CSRF保护
    WTF_CSRF_TIME_LIMIT = int(os.environ.get('WTF_CSRF_TIME_LIMIT', '3600'))
    
    # API安全
    API_RATE_LIMIT = os.environ.get('API_RATE_LIMIT', '1000 per hour')
    API_KEY_HEADER = os.environ.get('API_KEY_HEADER', 'X-API-Key')
    
    # CORS设置
    CORS_ORIGINS = os.environ.get('CORS_ORIGINS', '*').split(',')
    
    # 内容安全策略
    CSP_POLICY = {
        'default-src': "'self'",
        'script-src': "'self' 'unsafe-inline' 'unsafe-eval'",
        'style-src': "'self' 'unsafe-inline'",
        'img-src': "'self' data: https:",
        'font-src': "'self' data:",
        'connect-src': "'self'",
        'frame-ancestors': "'none'"
    }
    
    # 安全头设置
    SECURITY_HEADERS = {
        'X-Content-Type-Options': 'nosniff',
        'X-Frame-Options': 'DENY',
        'X-XSS-Protection': '1; mode=block',
        'Strict-Transport-Security': 'max-age=31536000; includeSubDomains',
        'Referrer-Policy': 'strict-origin-when-cross-origin'
    }
    
    # 请求限制
    MAX_CONTENT_LENGTH = int(os.environ.get('MAX_CONTENT_LENGTH', 16 * 1024 * 1024))  # 16MB
    MAX_FORM_MEMORY_SIZE = int(os.environ.get('MAX_FORM_MEMORY_SIZE', 2 * 1024 * 1024))  # 2MB
    
    # 日志安全
    LOG_SENSITIVE_DATA = os.environ.get('LOG_SENSITIVE_DATA', 'False').lower() == 'true'
    
    # 加密设置
    ENCRYPTION_ALGORITHM = os.environ.get('ENCRYPTION_ALGORITHM', 'AES-256-CBC')
    
    @classmethod
    def get_csp_string(cls):
        """获取CSP策略字符串"""
        return '; '.join([f"{k} {v}" for k, v in cls.CSP_POLICY.items()])