# guzi_backend/models/watchlist.py

from datetime import datetime
from ..database import db

class UserWatchlist(db.Model):
    """用户自选股模型"""
    __tablename__ = 'user_watchlist'

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True, comment='用户ID')
    stock_code = db.Column(db.String(20), db.ForeignKey('stocks.code'), primary_key=True, comment='股票代码')
    added_at = db.Column(db.DateTime(timezone=True), default=datetime.utcnow, comment='添加时间')

    # 定义与User和Stock模型的关系
    user = db.relationship('User', backref=db.backref('watchlist_items', lazy=True))
    stock = db.relationship('Stock', backref=db.backref('watchlist_users', lazy=True))

    def __repr__(self):
        return f'<UserWatchlist UserID:{self.user_id} Stock:{self.stock_code}>'
