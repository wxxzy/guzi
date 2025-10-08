from flask import Blueprint, jsonify, request
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from models import db, Stock, AnalysisResult
from services.analysis_service import perform_analysis

analysis_bp = Blueprint('analysis', __name__)
limiter = Limiter(key_func=get_remote_address, default_limits=["1000 per hour"])

@analysis_bp.route('/api/analysis/dragon', methods=['POST'])
@limiter.limit("30 per minute")
def analyze_dragon_stocks():
    """分析板块龙一龙二 (同步版本)"""
    try:
        data = request.get_json()
        sector = data.get('sector', '')  # 行业板块
        
        print(f"DEBUG: analyze_dragon_stocks endpoint called with sector: {sector}")
        result = perform_analysis('dragon', {'sector': sector})
        print(f"DEBUG: analyze_dragon_stocks completed")
        
        return jsonify(result)
    except Exception as e:
        print(f"DEBUG: analyze_dragon_stocks error: {str(e)}")
        return jsonify({'error': str(e)}), 500

@analysis_bp.route('/api/analysis/institutional', methods=['POST'])
@limiter.limit("30 per minute")
def analyze_institutional_stocks():
    """分析机构重仓股"""
    try:
        data = request.get_json()
        filters = data.get('filters', {})
        
        result = perform_analysis('institutional', {'filters': filters})
        
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@analysis_bp.route('/api/analysis/small_cap_leader', methods=['POST'])
@limiter.limit("30 per minute")
def analyze_small_cap_leader():
    """分析中小票龙头股"""
    try:
        data = request.get_json()
        max_market_cap = data.get('max_market_cap', 10000000000)  # 默认100亿市值以下
        
        result = perform_analysis('small_cap_leader', {'max_market_cap': max_market_cap})
        
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@analysis_bp.route('/api/analysis/small_cap_hot', methods=['POST'])
@limiter.limit("30 per minute")
def analyze_small_cap_hot():
    """分析小票热门股"""
    try:
        data = request.get_json()
        max_market_cap = data.get('max_market_cap', 5000000000)  # 默认50亿市值以下
        
        result = perform_analysis('small_cap_hot', {'max_market_cap': max_market_cap})
        
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@analysis_bp.route('/api/analysis/undervalued', methods=['POST'])
@limiter.limit("30 per minute")
def analyze_undervalued_stocks():
    """分析低估股票"""
    try:
        data = request.get_json()
        criteria = data.get('criteria', {})
        
        result = perform_analysis('undervalued', {'criteria': criteria})
        
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@analysis_bp.route('/api/analysis/comprehensive_score', methods=['POST'])
@limiter.limit("50 per minute")
def get_comprehensive_score():
    """获取股票综合评分"""
    try:
        data = request.get_json()
        symbol = data.get('symbol', '')
        
        result = perform_analysis('comprehensive_score', {'symbol': symbol})
        
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@analysis_bp.route('/api/analysis/stock_ranking', methods=['POST'])
@limiter.limit("20 per minute")
def get_stock_rankings():
    """获取股票排名"""
    try:
        data = request.get_json()
        limit = data.get('limit', 20)
        
        result = perform_analysis('stock_ranking', {'limit': limit})
        
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@analysis_bp.route('/api/analysis/natural_language', methods=['POST'])
@limiter.limit("30 per minute")
def natural_language_query():
    """自然语言查询"""
    try:
        data = request.get_json()
        query = data.get('query', '')
        user_context = data.get('user_context', {})
        
        result = perform_analysis('natural_language_query', {
            'query': query,
            'user_context': user_context
        })
        
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@analysis_bp.route('/api/analysis/personalized_recommendation', methods=['POST'])
@limiter.limit("20 per minute")
def personalized_recommendation():
    """个性化推荐"""
    try:
        data = request.get_json()
        user_profile = data.get('user_profile', {})
        
        result = perform_analysis('personalized_recommendation', {'user_profile': user_profile})
        
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@analysis_bp.route('/api/analysis/sentiment_analysis', methods=['POST'])
@limiter.limit("50 per minute")
def sentiment_analysis():
    """情绪分析"""
    try:
        data = request.get_json()
        text = data.get('text', '')
        
        result = perform_analysis('sentiment_analysis', {'text': text})
        
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@analysis_bp.route('/api/analysis/market_trend', methods=['GET'])
@limiter.limit("10 per minute")
def analyze_market_trend():
    """分析市场整体趋势"""
    try:
        result = perform_analysis('market_trend', {})
        
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@analysis_bp.route('/api/analysis/<symbol>/ai', methods=['POST'])
@limiter.limit("20 per minute")
def ai_stock_analysis(symbol):
    """使用AI进行个股深度分析"""
    try:
        data = request.get_json()
        analysis_type = data.get('type', 'comprehensive')
        
        result = perform_analysis('ai_analysis', {
            'symbol': symbol,
            'type': analysis_type
        })
        
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500