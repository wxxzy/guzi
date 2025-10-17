# guzi_backend/routes/watchlist.py

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from sqlalchemy.exc import IntegrityError
from ..database import db
from ..models import User, Stock, UserWatchlist

watchlist_bp = Blueprint('watchlist', __name__, url_prefix='/api/v1/watchlist')

@watchlist_bp.route('/', methods=['GET'])
@jwt_required()
def get_watchlist():
    """获取当前用户的自选股列表。"""
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)

    if not user:
        return jsonify({"code": 40401, "message": "User not found"}), 404

    # 通过关系加载自选股
    watchlist_stocks = [
        {
            "code": item.stock.code,
            "name": item.stock.name,
            "industry": item.stock.industry,
            "added_at": item.added_at.isoformat()
        }
        for item in user.watchlist_items
    ]

    return jsonify({"code": 0, "message": "Success", "data": {"watchlist": watchlist_stocks}}), 200

@watchlist_bp.route('/', methods=['POST'])
@jwt_required()
def add_to_watchlist():
    """添加股票到用户的自选股列表。"""
    current_user_id = get_jwt_identity()
    data = request.get_json()
    stock_code = data.get('stock_code')

    if not stock_code:
        return jsonify({"code": 40001, "message": "Stock code is required"}), 400

    stock = Stock.query.get(stock_code)
    if not stock:
        return jsonify({"code": 40402, "message": "Stock not found"}), 404

    try:
        new_item = UserWatchlist(user_id=current_user_id, stock_code=stock_code)
        db.session.add(new_item)
        db.session.commit()
        return jsonify({"code": 0, "message": "Stock added to watchlist"}), 201
    except IntegrityError:
        db.session.rollback()
        return jsonify({"code": 40901, "message": "Stock already in watchlist"}), 409
    except Exception as e:
        db.session.rollback()
        return jsonify({"code": 50001, "message": f"Failed to add stock to watchlist: {e}"}), 500

@watchlist_bp.route('/<string:stock_code>', methods=['DELETE'])
@jwt_required()
def remove_from_watchlist(stock_code):
    """从用户的自选股列表移除股票。"""
    current_user_id = get_jwt_identity()

    item = UserWatchlist.query.filter_by(user_id=current_user_id, stock_code=stock_code).first()

    if not item:
        return jsonify({"code": 40403, "message": "Stock not found in watchlist"}), 404

    try:
        db.session.delete(item)
        db.session.commit()
        return jsonify({"code": 0, "message": "Stock removed from watchlist"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"code": 50002, "message": f"Failed to remove stock from watchlist: {e}"}), 500
