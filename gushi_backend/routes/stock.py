from flask import Blueprint, jsonify, request
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from models import db, Stock, StockData
import akshare as ak

stock_bp = Blueprint('stock', __name__)
limiter = Limiter(key_func=get_remote_address, default_limits=["1000 per hour"])

@stock_bp.route('/api/stock/list')
@limiter.limit("500 per minute")
def get_stock_list():
    """获取股票列表"""
    try:
        stocks = Stock.query.all()
        return jsonify([stock.to_dict() for stock in stocks])
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@stock_bp.route('/api/stock/<symbol>')
@limiter.limit("100 per minute")
def get_stock_detail(symbol):
    """获取股票详情"""
    try:
        stock = Stock.query.filter_by(symbol=symbol).first()
        if not stock:
            return jsonify({'error': '股票不存在'}), 404
        return jsonify(stock.to_dict())
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@stock_bp.route('/api/stock/<symbol>/history')
@limiter.limit("50 per minute")
def get_stock_history(symbol):
    """获取股票历史数据"""
    try:
        # 获取日期范围参数
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        
        query = StockData.query.filter(StockData.stock_symbol == symbol)
        
        if start_date:
            from datetime import datetime
            start = datetime.strptime(start_date, '%Y-%m-%d').date()
            query = query.filter(StockData.date >= start)
        
        if end_date:
            from datetime import datetime
            end = datetime.strptime(end_date, '%Y-%m-%d').date()
            query = query.filter(StockData.date <= end)
        
        # 按日期排序，获取最新的数据
        stock_data = query.order_by(StockData.date.desc()).all()
        
        return jsonify([data.to_dict() for data in stock_data])
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@stock_bp.route('/api/stock/sync')
@limiter.limit("5 per minute")  # 数据同步操作限制频率
def sync_stock_data():
    """同步股票数据到数据库"""
    try:
        # 这里实现从AkShare同步数据的逻辑
        # 示例：获取沪深A股列表
        stock_info = ak.stock_info_sh_name_code()  # 上海A股
        stock_info_sz = ak.stock_info_sz_name_code()  # 深圳A股
        stock_info_bj = ak.stock_info_bj_name_code()  # 北京A股
        
        import pandas as pd
        all_stocks = pd.concat([stock_info, stock_info_sz, stock_info_bj], ignore_index=True)
        
        # 更新数据库中的股票信息
        for _, row in all_stocks.iterrows():
            # 根据AkShare返回的数据格式调整
            symbol = row.get('code', row.get('证券代码', ''))
            name = row.get('name', row.get('证券简称', ''))
            
            # 尝试查找已存在的股票记录
            stock = Stock.query.filter_by(symbol=symbol).first()
            if stock:
                # 更新现有记录
                stock.name = name
            else:
                # 创建新记录
                stock = Stock(symbol=symbol, name=name)
                db.session.add(stock)
        
        db.session.commit()
        
        return jsonify({
            'message': '股票数据同步完成',
            'total_stocks': len(all_stocks)
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500