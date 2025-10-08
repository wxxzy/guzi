"""
监控配置
"""
import os
from datetime import datetime
from typing import Dict, Any

class MonitoringConfig:
    """监控配置类"""
    
    # 日志配置
    LOG_LEVEL = os.environ.get('MONITORING_LOG_LEVEL', 'INFO')
    LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    LOG_FILE = os.environ.get('MONITORING_LOG_FILE', './logs/monitoring.log')
    
    # 性能监控
    ENABLE_PERFORMANCE_MONITORING = os.environ.get('ENABLE_PERFORMANCE_MONITORING', 'True').lower() == 'true'
    PERFORMANCE_LOG_INTERVAL = int(os.environ.get('PERFORMANCE_LOG_INTERVAL', '60'))  # 秒
    
    # 健康检查
    HEALTH_CHECK_INTERVAL = int(os.environ.get('HEALTH_CHECK_INTERVAL', '30'))  # 秒
    HEALTH_CHECK_TIMEOUT = int(os.environ.get('HEALTH_CHECK_TIMEOUT', '10'))  # 秒
    
    # 警报配置
    ENABLE_ALERTS = os.environ.get('ENABLE_ALERTS', 'True').lower() == 'true'
    ALERT_EMAIL_RECIPIENTS = os.environ.get('ALERT_EMAIL_RECIPIENTS', '').split(',')
    ALERT_WEBHOOK_URL = os.environ.get('ALERT_WEBHOOK_URL', '')
    
    # 指标收集
    METRICS_COLLECTION_INTERVAL = int(os.environ.get('METRICS_COLLECTION_INTERVAL', '60'))  # 秒
    ENABLE_DATABASE_METRICS = os.environ.get('ENABLE_DATABASE_METRICS', 'True').lower() == 'true'
    ENABLE_API_METRICS = os.environ.get('ENABLE_API_METRICS', 'True').lower() == 'true'
    
    # 存储配置
    METRICS_STORAGE_TYPE = os.environ.get('METRICS_STORAGE_TYPE', 'file')  # file, database, influxdb
    METRICS_RETENTION_DAYS = int(os.environ.get('METRICS_RETENTION_DAYS', '30'))
    
    # 自定义指标
    CUSTOM_METRICS = {
        'api_response_time': {
            'threshold': 5.0,  # 秒
            'description': 'API响应时间'
        },
        'database_connection_pool': {
            'threshold': 80,  # 百分比
            'description': '数据库连接池使用率'
        },
        'memory_usage': {
            'threshold': 80,  # 百分比
            'description': '内存使用率'
        },
        'cpu_usage': {
            'threshold': 80,  # 百分比
            'description': 'CPU使用率'
        }
    }
    
    @classmethod
    def get_metric_threshold(cls, metric_name: str) -> float:
        """获取指标阈值"""
        metric_config = cls.CUSTOM_METRICS.get(metric_name, {})
        return metric_config.get('threshold', 0)
    
    @classmethod
    def get_metric_description(cls, metric_name: str) -> str:
        """获取指标描述"""
        metric_config = cls.CUSTOM_METRICS.get(metric_name, {})
        return metric_config.get('description', metric_name)