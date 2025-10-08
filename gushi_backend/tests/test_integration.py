"""
集成测试套件
"""
import unittest
import os
import sys
from unittest.mock import patch, MagicMock

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app
from models import db, Stock
from services.analysis_service import perform_analysis


class TestIntegration(unittest.TestCase):
    """集成测试"""
    
    def setUp(self):
        """测试前准备"""
        self.app = create_app()
        self.app.config['TESTING'] = True
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'  # 使用内存数据库
        self.client = self.app.test_client()
        
        with self.app.app_context():
            db.create_all()
            # 创建测试数据
            test_stock = Stock(
                symbol='TEST001',
                name='测试股票',
                industry='金融',
                market_cap=10000000000,
                pe_ratio=10.0,
                pb_ratio=1.0
            )
            db.session.add(test_stock)
            db.session.commit()
    
    def test_app_health_endpoint(self):
        """测试应用健康检查端点"""
        response = self.client.get('/health')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data['status'], 'healthy')
    
    def test_stock_list_endpoint(self):
        """测试股票列表端点"""
        response = self.client.get('/api/stock/list')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIsInstance(data, list)
    
    def test_stock_detail_endpoint(self):
        """测试股票详情端点"""
        response = self.client.get('/api/stock/000001')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        if data:  # 如果数据存在
            self.assertEqual(data['symbol'], '000001')
    
    def test_perform_analysis_dragon(self):
        """测试龙一龙二分析功能"""
        with self.app.app_context():
            result = perform_analysis('dragon', {'sector': ''})
            self.assertIsInstance(result, dict)
            self.assertIn('timestamp', result)
            # 对于集成测试，我们主要验证函数能够正常执行
            # 实际的分析结果可能因数据而异
    
    def test_perform_analysis_institutional(self):
        """测试机构重仓股分析功能"""
        with self.app.app_context():
            result = perform_analysis('institutional', {'filters': {}})
            self.assertIsInstance(result, dict)
            self.assertIn('timestamp', result)
    
    def test_perform_analysis_undervalued(self):
        """测试低估股票分析功能"""
        with self.app.app_context():
            result = perform_analysis('undervalued', {'criteria': {}})
            self.assertIsInstance(result, dict)
            self.assertIn('timestamp', result)
    
    def test_perform_analysis_small_cap_leader(self):
        """测试中小票龙头股分析功能"""
        with self.app.app_context():
            result = perform_analysis('small_cap_leader', {'max_market_cap': 10000000000})
            self.assertIsInstance(result, dict)
            self.assertIn('timestamp', result)
    
    def test_perform_analysis_comprehensive_score(self):
        """测试综合评分功能"""
        with self.app.app_context():
            result = perform_analysis('comprehensive_score', {'symbol': '000001'})
            self.assertIsInstance(result, dict)
            if 'error' not in result:  # 如果没有错误
                self.assertIn('comprehensive_analysis', result)
    
    @patch('ai_services.mock_ai_service.MockAIService.get_mock_response')
    def test_perform_analysis_natural_language_query(self, mock_get_response):
        """测试自然语言查询功能（使用模拟）"""
        mock_get_response.return_value = "这是一个模拟的AI响应"
        
        with self.app.app_context():
            result = perform_analysis('natural_language_query', {
                'query': '000001股票怎么样',
                'user_context': {}
            })
            self.assertIsInstance(result, dict)
            # 验证返回了正确的类型
            self.assertIn('type', result)
    
    @patch('ai_services.mock_ai_service.MockAIService.get_mock_response')
    def test_perform_analysis_personalized_recommendation(self, mock_get_response):
        """测试个性化推荐功能（使用模拟）"""
        mock_get_response.return_value = "这是一个模拟的推荐结果"
        
        with self.app.app_context():
            result = perform_analysis('personalized_recommendation', {
                'user_profile': {
                    'risk_tolerance': 'medium',
                    'investment_goal': 'balanced'
                }
            })
            self.assertIsInstance(result, dict)
            # 验证返回了正确的类型
            self.assertIn('type', result)


class TestAnalysisServiceIntegration(unittest.TestCase):
    """分析服务集成测试"""
    
    def setUp(self):
        """测试前准备"""
        self.app = create_app()
        self.app.config['TESTING'] = True
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        
        with self.app.app_context():
            db.create_all()
            # 创建测试数据
            test_stock = Stock(
                symbol='TEST001',
                name='测试股票',
                industry='金融',
                market_cap=10000000000,
                pe_ratio=10.0,
                pb_ratio=1.0
            )
            db.session.add(test_stock)
            db.session.commit()
    
    def test_analysis_service_functions(self):
        """测试分析服务各项功能"""
        with self.app.app_context():
            # 测试各项分析功能是否能正常执行（不依赖真实数据）
            
            # 龙一龙二分析
            dragon_result = perform_analysis('dragon', {'sector': '金融'})
            self.assertIsInstance(dragon_result, dict)
            
            # 机构重仓股分析
            institutional_result = perform_analysis('institutional', {'filters': {}})
            self.assertIsInstance(institutional_result, dict)
            
            # 低估股票分析
            undervalued_result = perform_analysis('undervalued', {'criteria': {}})
            self.assertIsInstance(undervalued_result, dict)


if __name__ == '__main__':
    unittest.main()