from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Stock(db.Model):
    __tablename__ = 'stocks'
    
    id = db.Column(db.Integer, primary_key=True)
    symbol = db.Column(db.String(20), unique=True, nullable=False, index=True)
    name = db.Column(db.String(100), nullable=False)
    industry = db.Column(db.String(100))
    market_cap = db.Column(db.Float)  # 市值
    pe_ratio = db.Column(db.Float)    # 市盈率
    pb_ratio = db.Column(db.Float)    # 市净率
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # 与StockData建立关系
    stock_data = db.relationship('StockData', backref='stock', lazy=True)
    analysis_results = db.relationship('AnalysisResult', backref='stock', lazy=True)

    def to_dict(self):
        return {
            'id': self.id,
            'symbol': self.symbol,
            'name': self.name,
            'industry': self.industry,
            'market_cap': self.market_cap,
            'pe_ratio': self.pe_ratio,
            'pb_ratio': self.pb_ratio,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

class StockData(db.Model):
    __tablename__ = 'stock_data'
    
    id = db.Column(db.Integer, primary_key=True)
    stock_symbol = db.Column(db.String(20), db.ForeignKey('stocks.symbol'), nullable=False, index=True)
    date = db.Column(db.Date, nullable=False, index=True)
    open_price = db.Column(db.Float)
    close_price = db.Column(db.Float)
    high_price = db.Column(db.Float)
    low_price = db.Column(db.Float)
    volume = db.Column(db.BigInteger)
    turnover = db.Column(db.Float)  # 成交额
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'stock_symbol': self.stock_symbol,
            'date': self.date.isoformat() if self.date else None,
            'open_price': self.open_price,
            'close_price': self.close_price,
            'high_price': self.high_price,
            'low_price': self.low_price,
            'volume': self.volume,
            'turnover': self.turnover
        }

class AnalysisResult(db.Model):
    __tablename__ = 'analysis_results'
    
    id = db.Column(db.Integer, primary_key=True)
    stock_symbol = db.Column(db.String(20), db.ForeignKey('stocks.symbol'), nullable=True, index=True)  # 可为空，因为有些分析可能不针对特定股票
    analysis_type = db.Column(db.String(50), nullable=False, index=True)  # 'dragon', 'institutional', 'small_cap_leader', 'undervalued', 'market_trend'
    result = db.Column(db.Text, nullable=False)  # 存储JSON格式的分析结果
    ai_model_used = db.Column(db.String(100))  # 使用的AI模型
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'stock_symbol': self.stock_symbol,
            'analysis_type': self.analysis_type,
            'result': self.result,
            'ai_model_used': self.ai_model_used,
            'created_at': self.created_at.isoformat()
        }