"""
监控系统初始化脚本
负责初始化和启动监控组件
"""
import logging
import logging.config
import os
from datetime import datetime

from monitoring.config import MonitoringConfig
from monitoring.metrics_collector import metrics_collector
from monitoring.health_checker import health_checker
from monitoring.alert_system import alert_system

def setup_monitoring_logging():
    """设置监控系统日志"""
    # 创建日志目录
    log_dir = os.path.dirname(MonitoringConfig.LOG_FILE)
    if log_dir and not os.path.exists(log_dir):
        os.makedirs(log_dir)
    
    # 配置日志
    logging_config = {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'standard': {
                'format': MonitoringConfig.LOG_FORMAT
            },
        },
        'handlers': {
            'default': {
                'level': MonitoringConfig.LOG_LEVEL,
                'formatter': 'standard',
                'class': 'logging.StreamHandler',
            },
            'file': {
                'level': MonitoringConfig.LOG_LEVEL,
                'formatter': 'standard',
                'class': 'logging.FileHandler',
                'filename': MonitoringConfig.LOG_FILE,
                'mode': 'a',
            },
        },
        'loggers': {
            '': {
                'handlers': ['default', 'file'],
                'level': MonitoringConfig.LOG_LEVEL,
                'propagate': False
            }
        }
    }
    
    logging.config.dictConfig(logging_config)

def initialize_monitoring_system():
    """初始化监控系统"""
    try:
        # 设置日志
        setup_monitoring_logging()
        
        logger = logging.getLogger(__name__)
        logger.info("开始初始化监控系统...")
        
        # 初始化指标收集器
        logger.info("初始化指标收集器...")
        # metrics_collector.start_collection()  # 延迟启动，由应用控制
        
        # 初始化健康检查器
        logger.info("初始化健康检查器...")
        # health_checker  # 已经初始化
        
        # 初始化警报系统
        logger.info("初始化警报系统...")
        # alert_system  # 已经初始化
        
        logger.info("监控系统初始化完成")
        
        return True
    except Exception as e:
        print(f"监控系统初始化失败: {e}")
        return False

def start_monitoring_services():
    """启动监控服务"""
    try:
        logger = logging.getLogger(__name__)
        logger.info("启动监控服务...")
        
        # 启动指标收集
        metrics_collector.start_collection()
        
        logger.info("监控服务已启动")
        return True
    except Exception as e:
        logger.error(f"启动监控服务失败: {e}")
        return False

def stop_monitoring_services():
    """停止监控服务"""
    try:
        logger = logging.getLogger(__name__)
        logger.info("停止监控服务...")
        
        # 停止指标收集
        metrics_collector.stop_collection()
        
        logger.info("监控服务已停止")
        return True
    except Exception as e:
        logger.error(f"停止监控服务失败: {e}")
        return False

def run_health_check():
    """执行一次健康检查"""
    try:
        logger = logging.getLogger(__name__)
        logger.info("执行健康检查...")
        
        result = health_checker.check_all_components()
        
        logger.info(f"健康检查完成，总体状态: {result.get('overall_status', 'unknown')}")
        return result
    except Exception as e:
        logger.error(f"执行健康检查失败: {e}")
        return None

if __name__ == '__main__':
    # 如果直接运行此脚本，初始化监控系统
    if initialize_monitoring_system():
        print("监控系统初始化成功")
    else:
        print("监控系统初始化失败")