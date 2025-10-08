"""
性能测试套件
"""
import unittest
import os
import sys
import time
from concurrent.futures import ThreadPoolExecutor
import threading

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app
from models import db, Stock
from services.analysis_service import perform_analysis
from services.scoring_service import calculate_comprehensive_score, rank_stocks_by_comprehensive_score


class TestPerformance(unittest.TestCase):
    """性能测试"""
    
    def setUp(self):
        """测试前准备"""
        self.app = create_app()
        self.app.config['TESTING'] = True
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        
        with self.app.app_context():
            db.create_all()
            # 创建测试数据
            for i in range(50):  # 创建50只测试股票
                stock = Stock(
                    symbol=f'TEST{i:03d}',
                    name=f'测试股票{i:03d}',
                    industry='金融' if i % 3 == 0 else '科技' if i % 3 == 1 else '消费',
                    market_cap=1000000000 + i * 100000000,
                    pe_ratio=10.0 + i * 0.1,
                    pb_ratio=1.0 + i * 0.01
                )
                db.session.add(stock)
            db.session.commit()
    
    def test_single_stock_analysis_performance(self):
        """测试单个股票分析性能"""
        with self.app.app_context():
            start_time = time.time()
            
            result = perform_analysis('comprehensive_score', {'symbol': 'TEST001'})
            
            end_time = time.time()
            execution_time = end_time - start_time
            
            print(f"单个股票综合评分执行时间: {execution_time:.4f}秒")
            
            # 通常应该在1秒内完成
            self.assertLess(execution_time, 2.0, f"执行时间过长: {execution_time}秒")
    
    def test_ranking_performance(self):
        """测试股票排名性能"""
        with self.app.app_context():
            start_time = time.time()
            
            result = rank_stocks_by_comprehensive_score(limit=20)
            
            end_time = time.time()
            execution_time = end_time - start_time
            
            print(f"20只股票排名执行时间: {execution_time:.4f}秒")
            
            # 排名计算可能涉及较多数据，给定合理时间限制
            self.assertLess(execution_time, 5.0, f"执行时间过长: {execution_time}秒")
    
    def test_concurrent_analysis_performance(self):
        """测试并发分析性能"""
        def analyze_stock(symbol):
            with self.app.app_context():
                try:
                    return perform_analysis('comprehensive_score', {'symbol': symbol})
                except Exception as e:
                    return str(e)
        
        # 并发执行多个分析任务
        symbols = ['TEST001', 'TEST002', 'TEST003', 'TEST004', 'TEST005']
        start_time = time.time()
        
        with ThreadPoolExecutor(max_workers=5) as executor:
            futures = [executor.submit(analyze_stock, symbol) for symbol in symbols]
            results = [future.result() for future in futures]
        
        end_time = time.time()
        execution_time = end_time - start_time
        
        print(f"并发分析5个股票执行时间: {execution_time:.4f}秒")
        print(f"平均每个分析时间: {execution_time/len(symbols):.4f}秒")
        
        # 并发执行的总时间应该小于串行执行的时间
        self.assertLess(execution_time, 10.0, f"并发执行时间过长: {execution_time}秒")
    
    def test_memory_usage_during_analysis(self):
        """测试分析过程中的内存使用"""
        import psutil
        import os
        
        # 获取当前进程信息
        process = psutil.Process(os.getpid())
        memory_before = process.memory_info().rss / 1024 / 1024  # MB
        
        with self.app.app_context():
            # 执行一些分析操作
            for i in range(10):
                perform_analysis('comprehensive_score', {'symbol': f'TEST{i:03d}'})
        
        memory_after = process.memory_info().rss / 1024 / 1024  # MB
        memory_increase = memory_after - memory_before
        
        print(f"内存使用增加: {memory_increase:.2f}MB")
        
        # 内存增加应该在合理范围内
        self.assertLess(memory_increase, 100, f"内存增加过多: {memory_increase}MB")
    
    def test_response_time_api_endpoint(self):
        """测试API端点响应时间"""
        with self.app.test_client() as client:
            start_time = time.time()
            
            response = client.get('/health')
            
            end_time = time.time()
            response_time = end_time - start_time
            
            print(f"API健康检查响应时间: {response_time:.4f}秒")
            
            self.assertEqual(response.status_code, 200)
            self.assertLess(response_time, 0.1, f"API响应时间过长: {response_time}秒")


class TestScalability(unittest.TestCase):
    """可扩展性测试"""
    
    def setUp(self):
        """测试前准备"""
        self.app = create_app()
        self.app.config['TESTING'] = True
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        
        with self.app.app_context():
            db.create_all()
    
    def test_large_dataset_performance(self):
        """测试大数据集性能"""
        with self.app.app_context():
            # 创建大量测试数据
            for i in range(200):  # 创建200只股票
                stock = Stock(
                    symbol=f'LG{i:04d}',
                    name=f'大数据测试股票{i:04d}',
                    industry='金融',
                    market_cap=1000000000,
                    pe_ratio=15.0,
                    pb_ratio=1.5
                )
                db.session.add(stock)
            db.session.commit()
            
            # 测试排名功能在大数据集上的表现
            start_time = time.time()
            result = rank_stocks_by_comprehensive_score(limit=50)
            end_time = time.time()
            
            execution_time = end_time - start_time
            print(f"200只股票中排名前50执行时间: {execution_time:.4f}秒")
            
            # 大数据集上的计算时间应该在可接受范围内
            self.assertLess(execution_time, 10.0, f"大数据集处理时间过长: {execution_time}秒")


if __name__ == '__main__':
    unittest.main()