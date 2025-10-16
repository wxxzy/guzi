# guzi_backend/routes/main.py

from flask import Blueprint, jsonify, current_app, request
from guzi_backend.services import data_service
from guzi_backend.services import analysis_service

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

@main.route('/api/v1/debug/gemini-generate')
def gemini_generate_debug():
    """一个用于调试的端点，调用Gemini生成文本。"""
    prompt = request.args.get('prompt', '你好')
    if not prompt:
        return jsonify({"code": 40001, "message": "Prompt parameter is required.", "data": None}), 400

    try:
        gemini_adapter = current_app.ai_manager.get_adapter('gemini')
        response_text = gemini_adapter.generate_text(prompt)
        return jsonify({"code": 0, "message": "Success", "data": {"response": response_text}})
    except ValueError as e:
        return jsonify({"code": 50002, "message": str(e), "data": None}), 500
    except Exception as e:
        return jsonify({"code": 50003, "message": f"AI service error: {e}", "data": None}), 500

@main.route('/api/v1/analysis/sector-leaders')
def get_sector_leaders():
    """获取指定行业的龙一龙二股票。"""
    industry_name = request.args.get('industry')
    if not industry_name:
        return jsonify({"code": 40001, "message": "Industry name parameter is required.", "data": None}), 400

    try:
        leaders = analysis_service.identify_sector_leaders(industry_name)
        if not leaders:
            return jsonify({"code": 40401, "message": f"No leaders found for industry: {industry_name}", "data": []}), 404
        return jsonify({"code": 0, "message": "Success", "data": {"industry": industry_name, "leaders": leaders}})
    except Exception as e:
        return jsonify({"code": 50004, "message": f"Analysis service error: {e}", "data": None}), 500
