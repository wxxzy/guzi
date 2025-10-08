"""
AI服务功能测试脚本（更新版）
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import create_app
from ai_services.ai_client import test_ai_connection, get_available_services
from ai_services.ai_manager import ai_manager
from ai_services.mock_ai_service import get_ai_response_with_fallback, MockAIService
from models import Stock

def test_ai_services():
    app = create_app()
    
    with app.app_context():
        print("=== AI服务功能测试 ===")
        
        # 测试1: 检查可用服务
        print("\n1. 检查可用AI服务...")
        available_services = get_available_services()
        print(f"可用服务: {available_services}")
        
        # 测试2: 测试各AI服务连接
        print("\n2. 测试AI服务连接...")
        for service in ['qwen', 'volc', 'openai']:
            if available_services.get(service, False):
                print(f"测试 {service} 服务连接...")
                result = test_ai_connection(service)
                print(f"  结果: {result}")
            else:
                print(f"  {service}: 未配置或不可用（将使用模拟服务）")
        
        # 测试3: 执行基础AI请求（使用回退机制）
        print("\n3. 执行基础AI请求测试（使用回退机制）...")
        test_prompt = "请简单介绍一下人工智能在金融分析中的应用，不超过50字。"
        try:
            response = get_ai_response_with_fallback(test_prompt, model_type='qwen')
            print(f"AI响应: {response[:100]}...")
            print(f"响应长度: {len(response)}")
        except Exception as e:
            print(f"AI请求失败: {str(e)}")
        
        # 测试4: 测试模拟AI服务
        print("\n4. 测试模拟AI服务...")
        mock_response = MockAIService.get_mock_response("请分析股票趋势")
        print(f"模拟服务响应长度: {len(mock_response)}")
        print(f"模拟响应预览: {mock_response[:100]}...")
        
        # 测试5: 使用AI管理器
        print("\n5. 测试AI管理器功能...")
        
        # 获取一只测试股票
        test_stock = Stock.query.first()
        if test_stock:
            print(f"使用测试股票: {test_stock.name}({test_stock.symbol})")
            
            try:
                # 测试股票分析
                print("  - 测试股票分析...")
                stock_analysis = ai_manager.analyze_stock(
                    symbol=test_stock.symbol,
                    company_name=test_stock.name,
                    financial_data={'pe': 15.5, 'pb': 1.8, 'roe': 0.15},
                    market_data={'price': 10.5, 'volume': 1000000},
                    analysis_type="comprehensive"
                )
                print(f"    分析结果长度: {len(stock_analysis) if stock_analysis else 0}")
                
                # 测试技术分析
                print("  - 测试技术分析...")
                tech_analysis = ai_manager.analyze_stock(
                    symbol=test_stock.symbol,
                    company_name=test_stock.name,
                    financial_data={'pe': 15.5, 'pb': 1.8, 'roe': 0.15},
                    market_data={'price': 10.5, 'volume': 1000000},
                    analysis_type="technical"
                )
                print(f"    技术分析结果长度: {len(tech_analysis) if tech_analysis else 0}")
                
                # 测试比较功能（需要两只股票）
                test_stocks = Stock.query.limit(2).all()
                if len(test_stocks) >= 2:
                    print("  - 测试股票比较...")
                    comparison = ai_manager.compare_stocks(
                        stock1_info=test_stocks[0].to_dict(),
                        stock2_info=test_stocks[1].to_dict()
                    )
                    print(f"    比较结果: {len(comparison)} 项")
                    if comparison and 'raw_response' in comparison[0]:
                        print(f"    比较结果长度: {len(comparison[0]['raw_response'])}")
                
                # 测试市场报告生成
                print("  - 测试市场报告生成...")
                market_report = ai_manager.generate_market_report(
                    market_data={'index': 3000, 'volume': 8000000000},
                    sector_data={'tech': 2.5, 'finance': -0.2}
                )
                print(f"    市场报告长度: {len(market_report) if market_report else 0}")
                
            except Exception as e:
                print(f"AI管理器功能测试失败: {str(e)}")
        else:
            print("数据库中没有股票数据，跳过AI管理器功能测试")
        
        # 测试6: 获取服务状态
        print("\n6. 获取AI服务状态...")
        status = ai_manager.get_service_status()
        print(f"服务状态: {status}")
        
        print("\n=== AI服务功能测试完成 ===")

if __name__ == "__main__":
    test_ai_services()