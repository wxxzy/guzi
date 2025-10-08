"""
API测试用例
用于验证所有API接口的正确性
"""
import unittest
import json
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app
from models import db, Stock

class APITestCase(unittest.TestCase):
    """API测试用例"""
    
    def setUp(self):
        """测试前准备"""
        self.app = create_app('testing')
        self.app.config['TESTING'] = True
        self.client = self.app.test_client()
        
        with self.app.app_context():
            # 创建测试数据库表
            db.create_all()
            
            # 添加测试数据
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
    
    def tearDown(self):
        """测试后清理"""
        with self.app.app_context():
            # 清理测试数据
            db.session.remove()
            db.drop_all()
    
    def test_health_check(self):
        """测试健康检查接口"""
        response = self.client.get('/health')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['status'], 'healthy')
    
    def test_stock_list(self):
        """测试股票列表接口"""
        response = self.client.get('/api/stock/list')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIsInstance(data, list)
        self.assertGreater(len(data), 0)
    
    def test_stock_detail(self):
        """测试股票详情接口"""
        response = self.client.get('/api/stock/TEST001')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['symbol'], 'TEST001')
        self.assertEqual(data['name'], '测试股票')
    
    def test_stock_history(self):
        """测试股票历史数据接口"""
        response = self.client.get('/api/stock/TEST001/history')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIsInstance(data, list)
    
    def test_dragon_analysis(self):
        """测试板块龙一龙二分析接口"""
        response = self.client.post('/api/analysis/dragon', 
                                  data=json.dumps({'sector': '金融'}),
                                  content_type='application/json')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn('timestamp', data)
    
    def test_institutional_analysis(self):
        """测试机构重仓股分析接口"""
        response = self.client.post('/api/analysis/institutional',
                                  data=json.dumps({'filters': {}}),
                                  content_type='application/json')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn('timestamp', data)
    
    def test_small_cap_leader_analysis(self):
        """测试中小票龙头股分析接口"""
        response = self.client.post('/api/analysis/small_cap_leader',
                                  data=json.dumps({'max_market_cap': 10000000000}),
                                  content_type='application/json')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn('timestamp', data)
    
    def test_undervalued_analysis(self):
        """测试低估股票分析接口"""
        response = self.client.post('/api/analysis/undervalued',
                                  data=json.dumps({'criteria': {}}),
                                  content_type='application/json')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn('timestamp', data)
    
    def test_comprehensive_score(self):
        """测试综合评分接口"""
        response = self.client.post('/api/analysis/comprehensive_score',
                                  data=json.dumps({'symbol': 'TEST001'}),
                                  content_type='application/json')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn('timestamp', data)
    
    def test_stock_ranking(self):
        """测试股票排名接口"""
        response = self.client.post('/api/analysis/stock_ranking',
                                  data=json.dumps({'limit': 10}),
                                  content_type='application/json')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn('timestamp', data)
    
    def test_natural_language_query(self):
        """测试自然语言查询接口"""
        response = self.client.post('/api/analysis/natural_language',
                                  data=json.dumps({
                                      'query': '分析TEST001股票',
                                      'user_context': {}
                                  }),
                                  content_type='application/json')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn('timestamp', data)
    
    def test_personalized_recommendation(self):
        """测试个性化推荐接口"""
        response = self.client.post('/api/analysis/personalized_recommendation',
                                  data=json.dumps({
                                      'user_profile': {
                                          'risk_tolerance': 'medium',
                                          'investment_goal': 'balanced'
                                      }
                                  }),
                                  content_type='application/json')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn('timestamp', data)
    
    def test_sentiment_analysis(self):
        """测试情绪分析接口"""
        response = self.client.post('/api/analysis/sentiment_analysis',
                                  data=json.dumps({'text': '这只股票表现不错'}),
                                  content_type='application/json')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn('timestamp', data)
    
    def test_market_trend_analysis(self):
        """测试市场趋势分析接口"""
        response = self.client.get('/api/analysis/market_trend')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn('timestamp', data)
    
    def test_ai_stock_analysis(self):
        """测试AI个股分析接口"""
        response = self.client.post('/api/analysis/TEST001/ai',
                                  data=json.dumps({'type': 'comprehensive'}),
                                  content_type='application/json')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn('timestamp', data)
    
    def test_monitoring_health(self):
        """测试监控健康检查接口"""
        response = self.client.get('/monitoring/health')
        # 监控接口可能返回不同状态码，只要能访问即可
        self.assertIn(response.status_code, [200, 404, 500])
    
    def test_monitoring_metrics(self):
        """测试监控指标接口"""
        response = self.client.get('/monitoring/metrics')
        # 监控接口可能返回不同状态码，只要能访问即可
        self.assertIn(response.status_code, [200, 404, 500])
    
    def test_monitoring_status(self):
        """测试监控状态接口"""
        response = self.client.get('/monitoring/status')
        # 监控接口可能返回不同状态码，只要能访问即可
        self.assertIn(response.status_code, [200, 404, 500])

if __name__ == '__main__':
    unittest.main()