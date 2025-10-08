"""
输入验证器
提供各种输入验证功能
"""
import re
from typing import Dict, Any, List, Tuple

class InputValidator:
    """输入验证器类"""
    
    # 正则表达式模式
    PATTERNS = {
        'email': r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$',
        'phone': r'^\+?[1-9]\d{1,14}$',
        'username': r'^[a-zA-Z0-9_]{3,20}$',
        'password': r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[a-zA-Z\d@$!%*?&]{8,}$',
        'stock_symbol': r'^[A-Z0-9]{6}$',  # 6位股票代码
        'date': r'^\d{4}-\d{2}-\d{2}$',
        'positive_integer': r'^[1-9]\d*$',
        'positive_float': r'^[0-9]*\.?[0-9]+$'
    }
    
    @classmethod
    def validate_email(cls, email: str) -> bool:
        """验证邮箱格式"""
        return bool(re.match(cls.PATTERNS['email'], email))
    
    @classmethod
    def validate_phone(cls, phone: str) -> bool:
        """验证手机号格式"""
        return bool(re.match(cls.PATTERNS['phone'], phone))
    
    @classmethod
    def validate_username(cls, username: str) -> bool:
        """验证用户名格式"""
        return bool(re.match(cls.PATTERNS['username'], username))
    
    @classmethod
    def validate_password(cls, password: str) -> Tuple[bool, List[str]]:
        """验证密码强度"""
        errors = []
        
        if len(password) < 8:
            errors.append("密码长度至少8位")
        
        if not re.search(r'[a-z]', password):
            errors.append("密码必须包含小写字母")
        
        if not re.search(r'[A-Z]', password):
            errors.append("密码必须包含大写字母")
        
        if not re.search(r'\d', password):
            errors.append("密码必须包含数字")
        
        if not re.search(r'[@$!%*?&]', password):
            errors.append("密码必须包含特殊字符(@$!%*?&)")
        
        return len(errors) == 0, errors
    
    @classmethod
    def validate_stock_symbol(cls, symbol: str) -> bool:
        """验证股票代码格式"""
        return bool(re.match(cls.PATTERNS['stock_symbol'], symbol))
    
    @classmethod
    def validate_date(cls, date: str) -> bool:
        """验证日期格式"""
        if not re.match(cls.PATTERNS['date'], date):
            return False
        
        # 进一步验证日期有效性
        try:
            from datetime import datetime
            datetime.strptime(date, '%Y-%m-%d')
            return True
        except ValueError:
            return False
    
    @classmethod
    def validate_positive_integer(cls, value: str) -> bool:
        """验证正整数"""
        return bool(re.match(cls.PATTERNS['positive_integer'], value))
    
    @classmethod
    def validate_positive_float(cls, value: str) -> bool:
        """验证正浮点数"""
        return bool(re.match(cls.PATTERNS['positive_float'], value))
    
    @classmethod
    def validate_json_payload(cls, data: Dict[str, Any], required_fields: List[str]) -> Tuple[bool, List[str]]:
        """验证JSON请求体"""
        errors = []
        
        # 检查必需字段
        for field in required_fields:
            if field not in data:
                errors.append(f"缺少必需字段: {field}")
        
        # 检查字段类型和值
        for key, value in data.items():
            if value is None:
                continue
                
            # 根据字段名进行特定验证
            if key == 'email' and isinstance(value, str):
                if not cls.validate_email(value):
                    errors.append(f"邮箱格式不正确: {value}")
            
            elif key == 'symbol' and isinstance(value, str):
                if not cls.validate_stock_symbol(value):
                    errors.append(f"股票代码格式不正确: {value}")
            
            elif key == 'date' and isinstance(value, str):
                if not cls.validate_date(value):
                    errors.append(f"日期格式不正确: {value}")
            
            elif key in ['amount', 'price'] and isinstance(value, (int, float)):
                if value < 0:
                    errors.append(f"{key}不能为负数: {value}")
        
        return len(errors) == 0, errors
    
    @classmethod
    def sanitize_string(cls, input_string: str, max_length: int = 1000) -> str:
        """清理字符串输入"""
        if not isinstance(input_string, str):
            return ""
        
        # 限制长度
        if len(input_string) > max_length:
            input_string = input_string[:max_length]
        
        # 移除控制字符
        input_string = ''.join(ch for ch in input_string if ord(ch) >= 32 or ch in '\n\r\t')
        
        # 转义HTML特殊字符
        import html
        input_string = html.escape(input_string)
        
        return input_string.strip()
    
    @classmethod
    def validate_and_sanitize_input(cls, data: Dict[str, Any]) -> Dict[str, Any]:
        """验证并清理输入数据"""
        sanitized_data = {}
        
        for key, value in data.items():
            if isinstance(value, str):
                # 清理字符串输入
                sanitized_value = cls.sanitize_string(value)
                sanitized_data[key] = sanitized_value
            else:
                # 其他类型直接保留
                sanitized_data[key] = value
        
        return sanitized_data