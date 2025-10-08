"""
监控指标收集器
负责收集和存储系统性能指标
"""
import time
import psutil
import logging
from datetime import datetime
from typing import Dict, Any, List
from threading import Thread
import json
import os

from monitoring.config import MonitoringConfig

class MetricsCollector:
    """指标收集器类"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.metrics_storage = []
        self.collecting = False
        self.collection_thread = None
        
    def start_collection(self):
        """开始收集指标"""
        if not self.collecting:
            self.collecting = True
            self.collection_thread = Thread(target=self._collect_metrics_loop)
            self.collection_thread.daemon = True
            self.collection_thread.start()
            self.logger.info("指标收集器已启动")
    
    def stop_collection(self):
        """停止收集指标"""
        self.collecting = False
        if self.collection_thread:
            self.collection_thread.join()
        self.logger.info("指标收集器已停止")
    
    def _collect_metrics_loop(self):
        """指标收集循环"""
        while self.collecting:
            try:
                metrics = self._collect_system_metrics()
                self._store_metrics(metrics)
                self.logger.debug(f"收集到系统指标: {metrics}")
                
                # 等待下次收集
                time.sleep(MonitoringConfig.METRICS_COLLECTION_INTERVAL)
            except Exception as e:
                self.logger.error(f"收集指标时出错: {e}")
                time.sleep(10)  # 出错后等待10秒再重试
    
    def _collect_system_metrics(self) -> Dict[str, Any]:
        """收集系统指标"""
        timestamp = datetime.now().isoformat()
        
        # CPU使用率
        cpu_percent = psutil.cpu_percent(interval=1)
        
        # 内存使用率
        memory = psutil.virtual_memory()
        memory_percent = memory.percent
        
        # 磁盘使用率
        disk = psutil.disk_usage('/')
        disk_percent = (disk.used / disk.total) * 100
        
        # 网络IO
        net_io = psutil.net_io_counters()
        bytes_sent = net_io.bytes_sent
        bytes_recv = net_io.bytes_recv
        
        # 系统负载
        try:
            load_avg = os.getloadavg()
        except OSError:
            load_avg = [0, 0, 0]
        
        return {
            'timestamp': timestamp,
            'cpu_percent': cpu_percent,
            'memory_percent': memory_percent,
            'disk_percent': disk_percent,
            'bytes_sent': bytes_sent,
            'bytes_recv': bytes_recv,
            'load_average_1min': load_avg[0],
            'load_average_5min': load_avg[1],
            'load_average_15min': load_avg[2]
        }
    
    def _store_metrics(self, metrics: Dict[str, Any]):
        """存储指标"""
        self.metrics_storage.append(metrics)
        
        # 限制存储大小，只保留最近的指标
        if len(self.metrics_storage) > 1000:
            self.metrics_storage = self.metrics_storage[-1000:]
        
        # 根据配置存储到文件或数据库
        if MonitoringConfig.METRICS_STORAGE_TYPE == 'file':
            self._store_to_file(metrics)
    
    def _store_to_file(self, metrics: Dict[str, Any]):
        """存储指标到文件"""
        try:
            log_dir = os.path.dirname(MonitoringConfig.LOG_FILE)
            if log_dir and not os.path.exists(log_dir):
                os.makedirs(log_dir)
            
            with open(MonitoringConfig.LOG_FILE.replace('.log', '_metrics.json'), 'a') as f:
                f.write(json.dumps(metrics) + '\n')
        except Exception as e:
            self.logger.error(f"存储指标到文件时出错: {e}")
    
    def get_recent_metrics(self, count: int = 10) -> List[Dict[str, Any]]:
        """获取最近的指标"""
        return self.metrics_storage[-count:] if self.metrics_storage else []
    
    def get_metrics_summary(self) -> Dict[str, Any]:
        """获取指标摘要"""
        if not self.metrics_storage:
            return {}
        
        recent_metrics = self.metrics_storage[-10:]  # 最近10个指标
        
        # 计算平均值
        cpu_avg = sum(m['cpu_percent'] for m in recent_metrics) / len(recent_metrics)
        memory_avg = sum(m['memory_percent'] for m in recent_metrics) / len(recent_metrics)
        disk_avg = sum(m['disk_percent'] for m in recent_metrics) / len(recent_metrics)
        
        latest = recent_metrics[-1]
        
        return {
            'latest_metrics': latest,
            'averages': {
                'cpu_percent': round(cpu_avg, 2),
                'memory_percent': round(memory_avg, 2),
                'disk_percent': round(disk_avg, 2)
            },
            'alert_status': self._check_alerts(latest)
        }
    
    def _check_alerts(self, metrics: Dict[str, Any]) -> Dict[str, Any]:
        """检查警报条件"""
        alerts = {}
        
        # CPU使用率警报
        cpu_threshold = MonitoringConfig.get_metric_threshold('cpu_usage')
        if metrics['cpu_percent'] > cpu_threshold:
            alerts['cpu'] = f"CPU使用率过高: {metrics['cpu_percent']}% > {cpu_threshold}%"
        
        # 内存使用率警报
        memory_threshold = MonitoringConfig.get_metric_threshold('memory_usage')
        if metrics['memory_percent'] > memory_threshold:
            alerts['memory'] = f"内存使用率过高: {metrics['memory_percent']}% > {memory_threshold}%"
        
        # 磁盘使用率警报
        disk_threshold = 90  # 磁盘使用率硬编码阈值
        if metrics['disk_percent'] > disk_threshold:
            alerts['disk'] = f"磁盘使用率过高: {metrics['disk_percent']}% > {disk_threshold}%"
        
        return alerts

# 创建全局指标收集器实例
metrics_collector = MetricsCollector()