from flask import Blueprint, jsonify
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

main_bp = Blueprint('main', __name__)
limiter = Limiter(key_func=get_remote_address, default_limits=["1000 per hour"])

@main_bp.route('/')
@limiter.limit("100 per minute")
def index():
    return jsonify({
        'message': '欢迎使用基于AI大模型的股票智能分析系统',
        'version': '1.0.0',
        'endpoints': {
            'stock_data': '/api/stock',
            'analysis': '/api/analysis'
        }
    })

@main_bp.route('/health')
@limiter.limit("200 per minute")
def health():
    return jsonify({'status': 'healthy'})