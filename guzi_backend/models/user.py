# guzi_backend/models/user.py

from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from ..database import db

class User(db.Model):
    """用户模型"""
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True, comment='主键ID')
    username = db.Column(db.String(50), unique=True, nullable=False, comment='用户名')
    email = db.Column(db.String(100), unique=True, nullable=False, comment='电子邮箱')
    password_hash = db.Column(db.String(255), nullable=False, comment='哈希处理后的密码')
    created_at = db.Column(db.DateTime(timezone=True), default=datetime.utcnow, comment='账户创建时间')

    def set_password(self, password):
        """设置用户密码，进行哈希处理。"""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """验证用户密码。"""
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<User {self.username}>'
