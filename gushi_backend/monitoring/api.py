"""
监控API端点
提供系统监控和健康检查的API接口
"""
from flask import Blueprint, jsonify, request
import logging
from datetime import datetime

from monitoring.metrics_collector import metrics_collector
from monitoring.health_checker import health_checker
from monitoring.alert_system import alert_system

# 创建监控蓝图
monitoring_bp = Blueprint('monitoring', __name__)
logger = logging.getLogger(__name__)

@monitoring_bp.route('/monitoring/health', methods=['GET'])
def health_check():
    """健康检查端点"""
    try:
        result = health_checker.check_all_components()
        return jsonify(result)
    except Exception as e:
        logger.error(f"健康检查失败: {e}")
        return jsonify({
            'status': 'error',
            'message': f'健康检查执行失败: {str(e)}',
            'timestamp': datetime.now().isoformat()
        }), 500

@monitoring_bp.route('/monitoring/metrics', methods=['GET'])
def get_metrics():
    """获取系统指标"""
    try:
        count = request.args.get('count', 10, type=int)
        metrics = metrics_collector.get_recent_metrics(count)
        summary = metrics_collector.get_metrics_summary()
        
        return jsonify({
            'metrics': metrics,
            'summary': summary,
            'timestamp': datetime.now().isoformat()
        })
    except Exception as e:
        logger.error(f"获取指标失败: {e}")
        return jsonify({
            'status': 'error',
            'message': f'获取指标失败: {str(e)}',
            'timestamp': datetime.now().isoformat()
        }), 500

@monitoring_bp.route('/monitoring/alerts', methods=['GET'])
def get_alerts():
    """获取警报历史"""
    try:
        limit = request.args.get('limit', 50, type=int)
        alerts = alert_system.get_alert_history(limit)
        
        return jsonify({
            'alerts': alerts,
            'timestamp': datetime.now().isoformat()
        })
    except Exception as e:
        logger.error(f"获取警报历史失败: {e}")
        return jsonify({
            'status': 'error',
            'message': f'获取警报历史失败: {str(e)}',
            'timestamp': datetime.now().isoformat()
        }), 500

@monitoring_bp.route('/monitoring/alerts/active', methods=['GET'])
def get_active_alerts():
    """获取活跃警报"""
    try:
        active_alerts = alert_system.get_active_alerts()
        
        return jsonify({
            'active_alerts': active_alerts,
            'count': len(active_alerts),
            'timestamp': datetime.now().isoformat()
        })
    except Exception as e:
        logger.error(f"获取活跃警报失败: {e}")
        return jsonify({
            'status': 'error',
            'message': f'获取活跃警报失败: {str(e)}',
            'timestamp': datetime.now().isoformat()
        }), 500

@monitoring_bp.route('/monitoring/status', methods=['GET'])
def get_system_status():
    """获取系统状态摘要"""
    try:
        # 获取健康状态
        health_summary = health_checker.get_health_summary()
        
        # 获取指标摘要
        metrics_summary = metrics_collector.get_metrics_summary()
        
        # 获取活跃警报
        active_alerts = alert_system.get_active_alerts()
        
        return jsonify({
            'health': health_summary,
            'metrics': metrics_summary,
            'alerts': {
                'active_count': len(active_alerts),
                'active_alerts': active_alerts[:5]  # 只返回前5个活跃警报
            },
            'timestamp': datetime.now().isoformat()
        })
    except Exception as e:
        logger.error(f"获取系统状态失败: {e}")
        return jsonify({
            'status': 'error',
            'message': f'获取系统状态失败: {str(e)}',
            'timestamp': datetime.now().isoformat()
        }), 500

@monitoring_bp.route('/monitoring/start-collecting', methods=['POST'])
def start_metrics_collection():
    """启动指标收集"""
    try:
        metrics_collector.start_collection()
        return jsonify({
            'status': 'success',
            'message': '指标收集已启动',
            'timestamp': datetime.now().isoformat()
        })
    except Exception as e:
        logger.error(f"启动指标收集失败: {e}")
        return jsonify({
            'status': 'error',
            'message': f'启动指标收集失败: {str(e)}',
            'timestamp': datetime.now().isoformat()
        }), 500

@monitoring_bp.route('/monitoring/stop-collecting', methods=['POST'])
def stop_metrics_collection():
    """停止指标收集"""
    try:
        metrics_collector.stop_collection()
        return jsonify({
            'status': 'success',
            'message': '指标收集已停止',
            'timestamp': datetime.now().isoformat()
        })
    except Exception as e:
        logger.error(f"停止指标收集失败: {e}")
        return jsonify({
            'status': 'error',
            'message': f'停止指标收集失败: {str(e)}',
            'timestamp': datetime.now().isoformat()
        }), 500

# 导出蓝图和组件实例
__all__ = ['monitoring_bp', 'metrics_collector', 'health_checker', 'alert_system']