# guzi_backend/models/stock.py

from ..database import db
from sqlalchemy.sql import func

class Stock(db.Model):
    """股票信息模型"""
    __tablename__ = 'stocks'

    # 根据数据库设计文档定义列
    code = db.Column(db.String(20), primary_key=True, comment='股票代码，全局唯一')
    name = db.Column(db.String(50), nullable=False, comment='股票名称')
    industry = db.Column(db.String(50), nullable=True, comment='所属行业')
    market = db.Column(db.String(10), nullable=False, comment='所属市场 (SH, SZ, HK, US)')
    is_active = db.Column(db.Boolean, default=True, comment='是否仍在上市交易')
    
    # 使用func.now()让数据库处理时间戳
    updated_at = db.Column(
        db.DateTime(timezone=True), 
        server_default=func.now(), 
        onupdate=func.now(),
        comment='信息最后更新时间'
    )

    def __repr__(self):
        return f'<Stock {self.code} {self.name}>'
