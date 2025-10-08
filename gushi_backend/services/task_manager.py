import uuid
import time
from datetime import datetime
from threading import Lock
from concurrent.futures import ThreadPoolExecutor, as_completed
import threading

# 全局任务状态存储
class TaskManager:
    def __init__(self):
        self._tasks = {}
        self._lock = Lock()
        self._executor = ThreadPoolExecutor(max_workers=2)  # 限制并发任务数
    
    def create_task(self, task_type, params):
        """创建一个新任务"""
        task_id = str(uuid.uuid4())
        
        with self._lock:
            self._tasks[task_id] = {
                'id': task_id,
                'type': task_type,
                'params': params,
                'status': 'pending',  # pending, running, completed, failed
                'progress': 0,
                'current_step': '初始化',
                'current_item': None,
                'result': None,
                'error': None,
                'created_at': datetime.now().isoformat(),
                'completed_at': None
            }
        
        # 提交任务到线程池
        future = self._executor.submit(self._execute_task, task_id)
        self._tasks[task_id]['future'] = future
        
        return task_id

    def get_task_status(self, task_id):
        """获取任务状态"""
        with self._lock:
            if task_id in self._tasks:
                task = self._tasks[task_id].copy()
                # 不返回future对象
                if 'future' in task:
                    del task['future']
                return task
            return None

    def update_task_progress(self, task_id, progress, current_step=None, current_item=None):
        """更新任务进度"""
        with self._lock:
            if task_id in self._tasks:
                self._tasks[task_id]['progress'] = progress
                if current_step:
                    self._tasks[task_id]['current_step'] = current_step
                if current_item:
                    self._tasks[task_id]['current_item'] = current_item
                self._tasks[task_id]['status'] = 'running'

    def complete_task(self, task_id, result):
        """完成任务"""
        with self._lock:
            if task_id in self._tasks:
                self._tasks[task_id]['status'] = 'completed'
                self._tasks[task_id]['result'] = result
                self._tasks[task_id]['progress'] = 100
                self._tasks[task_id]['completed_at'] = datetime.now().isoformat()

    def fail_task(self, task_id, error):
        """标记任务失败"""
        with self._lock:
            if task_id in self._tasks:
                self._tasks[task_id]['status'] = 'failed'
                self._tasks[task_id]['error'] = str(error)
                self._tasks[task_id]['completed_at'] = datetime.now().isoformat()
    
    def _execute_task(self, task_id):
        """执行任务的具体逻辑"""
        try:
            # 获取任务参数
            with self._lock:
                task_params = self._tasks[task_id]['params']
                task_type = self._tasks[task_id]['type']
            
            # 根据任务类型执行相应的分析
            if task_type == 'dragon':
                from services.analysis_service import analyze_sector_dragons_realtime
                result = analyze_sector_dragons_realtime(
                    task_params.get('sector', ''), 
                    task_id, 
                    self
                )
                self.complete_task(task_id, result)
            else:
                # 其他类型的任务
                self.fail_task(task_id, f"不支持的任务类型: {task_type}")
        except Exception as e:
            self.fail_task(task_id, str(e))

# 创建全局任务管理器实例
task_manager = TaskManager()