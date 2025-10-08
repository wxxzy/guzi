from flask import Blueprint, jsonify, request
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from services.task_manager import task_manager

task_bp = Blueprint('task', __name__)
limiter = Limiter(key_func=get_remote_address, default_limits=["1000 per hour"])

@task_bp.route('/api/task/start', methods=['POST'])
@limiter.limit("10 per minute")
def start_task():
    """启动一个新任务"""
    try:
        data = request.get_json()
        task_type = data.get('type')
        params = data.get('params', {})
        
        if not task_type:
            return jsonify({'error': '任务类型不能为空'}), 400
        
        task_id = task_manager.create_task(task_type, params)
        
        return jsonify({
            'task_id': task_id,
            'status': 'created',
            'message': f'任务 {task_type} 已创建'
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@task_bp.route('/api/task/status/<task_id>', methods=['GET'])
@limiter.limit("50 per minute")
def get_task_status(task_id):
    """获取任务状态"""
    try:
        task = task_manager.get_task_status(task_id)
        if not task:
            return jsonify({'error': '任务不存在'}), 404
        
        return jsonify(task)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@task_bp.route('/api/task/result/<task_id>', methods=['GET'])
@limiter.limit("50 per minute")
def get_task_result(task_id):
    """获取任务结果（阻塞直到完成）"""
    try:
        import time
        timeout = int(request.args.get('timeout', 300))  # 默认5分钟超时
        interval = float(request.args.get('interval', 1.0))  # 默认1秒检查一次
        
        start_time = time.time()
        while time.time() - start_time < timeout:
            task = task_manager.get_task_status(task_id)
            if not task:
                return jsonify({'error': '任务不存在'}), 404
            
            if task['status'] == 'completed':
                return jsonify(task)
            elif task['status'] == 'failed':
                return jsonify(task), 500
            
            time.sleep(interval)
        
        # 超时返回当前状态
        task = task_manager.get_task_status(task_id)
        return jsonify({
            'error': '任务超时',
            'task': task
        }), 408
    except Exception as e:
        return jsonify({'error': str(e)}), 500