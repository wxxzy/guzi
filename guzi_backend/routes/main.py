# guzi_backend/routes/main.py

from flask import Blueprint, jsonify
from guzi_backend.services import data_service

# 创建一个名为'main'的蓝图
main = Blueprint('main', __name__)

@main.route('/')
def index():
    """根路径，用于健康检查或欢迎页面。"""
    return "Welcome to the Guzi Backend! The application is running."

@main.route('/api/v1')
def api_base():
    """API基础路径，返回API信息。"""
    return jsonify({
        "code": 0,
        "message": "Success",
        "data": {
            "service": "Guzi Stock Analysis API",
            "version": "v1"
        }
    })

@main.route('/api/v1/debug/all-stocks')
def get_all_stocks_debug():
    """一个用于调试的端点，获取所有A股列表。"""
    stocks_df = data_service.get_all_stocks()
    if stocks_df.empty:
        return jsonify({
            "code": 50001,
            "message": "Failed to fetch stock list from data source.",
            "data": None
        }), 500
    
    # 将DataFrame转换为JSON格式
    stocks_json = stocks_df.to_dict(orient='records')
    
    return jsonify({
        "code": 0,
        "message": "Success",
        "data": {
            "count": len(stocks_json),
            "stocks": stocks_json
        }
    })
