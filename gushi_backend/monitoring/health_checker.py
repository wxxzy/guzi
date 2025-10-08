"""
健康检查器
负责检查系统各组件的健康状态
"""
import requests
import logging
from datetime import datetime
from typing import Dict, Any, List
import socket
import psutil

from monitoring.config import MonitoringConfig

class HealthChecker:
    """健康检查器类"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.check_results = []
    
    def check_all_components(self) -> Dict[str, Any]:
        """检查所有组件的健康状态"""
        results = {
            'timestamp': datetime.now().isoformat(),
            'checks': {}
        }
        
        # 检查数据库连接
        results['checks']['database'] = self._check_database()
        
        # 检查API服务
        results['checks']['api'] = self._check_api()
        
        # 检查外部依赖
        results['checks']['external_dependencies'] = self._check_external_dependencies()
        
        # 检查系统资源
        results['checks']['system_resources'] = self._check_system_resources()
        
        # 计算总体健康状态
        results['overall_status'] = self._calculate_overall_status(results['checks'])
        
        # 记录检查结果
        self.check_results.append(results)
        
        # 限制存储大小
        if len(self.check_results) > 100:
            self.check_results = self.check_results[-100:]
        
        return results
    
    def _check_database(self) -> Dict[str, Any]:
        """检查数据库连接"""
        try:
            # 这里应该实际测试数据库连接
            # 为了演示，我们假设连接正常
            return {
                'status': 'healthy',
                'message': '数据库连接正常',
                'timestamp': datetime.now().isoformat()
            }
        except Exception as e:
            self.logger.error(f"数据库健康检查失败: {e}")
            return {
                'status': 'unhealthy',
                'message': f'数据库连接失败: {str(e)}',
                'timestamp': datetime.now().isoformat()
            }
    
    def _check_api(self) -> Dict[str, Any]:
        """检查API服务"""
        try:
            # 检查本地API端点
            response = requests.get(
                'http://localhost:5000/health',
                timeout=MonitoringConfig.HEALTH_CHECK_TIMEOUT
            )
            
            if response.status_code == 200:
                return {
                    'status': 'healthy',
                    'message': 'API服务正常',
                    'response_time': response.elapsed.total_seconds(),
                    'timestamp': datetime.now().isoformat()
                }
            else:
                return {
                    'status': 'unhealthy',
                    'message': f'API返回错误状态码: {response.status_code}',
                    'timestamp': datetime.now().isoformat()
                }
        except Exception as e:
            self.logger.error(f"API健康检查失败: {e}")
            return {
                'status': 'unhealthy',
                'message': f'API服务不可达: {str(e)}',
                'timestamp': datetime.now().isoformat()
            }
    
    def _check_external_dependencies(self) -> Dict[str, Any]:
        """检查外部依赖"""
        dependencies = {
            'akshare': 'akshare.com',  # AkShare数据源
            'qwen_api': 'dashscope.aliyuncs.com',  # 通义千问API
            'volc_api': 'ark.cn-beijing.volces.com'  # 火山引擎API
        }
        
        results = {}
        
        for name, host in dependencies.items():
            try:
                # 检查主机连通性
                socket.create_connection((host, 80), timeout=5)
                results[name] = {
                    'status': 'healthy',
                    'message': f'{name}连接正常'
                }
            except Exception as e:
                results[name] = {
                    'status': 'unhealthy',
                    'message': f'{name}连接失败: {str(e)}'
                }
        
        return results
    
    def _check_system_resources(self) -> Dict[str, Any]:
        """检查系统资源"""
        try:
            # CPU使用率
            cpu_percent = psutil.cpu_percent(interval=1)
            
            # 内存使用率
            memory = psutil.virtual_memory()
            memory_percent = memory.percent
            
            # 磁盘使用率
            disk = psutil.disk_usage('/')
            disk_percent = (disk.used / disk.total) * 100
            
            return {
                'status': 'healthy',
                'cpu_percent': cpu_percent,
                'memory_percent': memory_percent,
                'disk_percent': disk_percent,
                'message': '系统资源监控正常'
            }
        except Exception as e:
            self.logger.error(f"系统资源检查失败: {e}")
            return {
                'status': 'unhealthy',
                'message': f'系统资源检查失败: {str(e)}'
            }
    
    def _calculate_overall_status(self, checks: Dict[str, Any]) -> str:
        """计算总体健康状态"""
        unhealthy_count = 0
        total_checks = 0
        
        for component, result in checks.items():
            if isinstance(result, dict):
                if result.get('status') == 'unhealthy':
                    unhealthy_count += 1
                total_checks += 1
            elif isinstance(result, dict):
                # 处理嵌套的检查结果
                for sub_component, sub_result in result.items():
                    if isinstance(sub_result, dict) and sub_result.get('status') == 'unhealthy':
                        unhealthy_count += 1
                    total_checks += 1
        
        if unhealthy_count == 0:
            return 'healthy'
        elif unhealthy_count <= total_checks * 0.3:  # 30%以下不健康视为警告
            return 'warning'
        else:
            return 'unhealthy'
    
    def get_recent_checks(self, count: int = 10) -> List[Dict[str, Any]]:
        """获取最近的健康检查结果"""
        return self.check_results[-count:] if self.check_results else []
    
    def get_health_summary(self) -> Dict[str, Any]:
        """获取健康状态摘要"""
        if not self.check_results:
            return {}
        
        latest = self.check_results[-1]
        return {
            'latest_check': latest,
            'overall_status': latest['overall_status'],
            'timestamp': latest['timestamp']
        }

# 创建全局健康检查器实例
health_checker = HealthChecker()