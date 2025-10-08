"""
股票分析功能测试脚本
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import create_app
from services.analysis_service import perform_analysis
from models import Stock

def test_stock_analysis():
    app = create_app()
    
    with app.app_context():
        print("=== 股票分析功能测试 ===")
        
        # 获取测试股票
        test_stock = Stock.query.first()
        if not test_stock:
            print("数据库中没有股票数据，跳过测试")
            return
        
        test_symbol = test_stock.symbol
        print(f"使用测试股票: {test_stock.name}({test_symbol})")
        
        # 测试1: 板块龙一龙二分析
        print("\n1. 测试板块龙一龙二分析...")
        try:
            dragon_result = perform_analysis('dragon', {'sector': ''})  # 空sector表示全市场
            print(f"   结果数量: {len(dragon_result.get('dragons', []))}")
            print(f"   龙头股: {[s['name'] for s in dragon_result.get('dragons', [])[:2]]}")
            if dragon_result.get('message'):
                print(f"   消息: {dragon_result['message']}")
        except Exception as e:
            print(f"   错误: {str(e)}")
        
        # 测试2: 机构重仓股分析
        print("\n2. 测试机构重仓股分析...")
        try:
            institutional_result = perform_analysis('institutional', {
                'min_market_cap': 5000000000,  # 50亿
                'min_roe': 0.08
            })
            print(f"   机构重仓股数量: {len(institutional_result.get('institutional_heavy_holding', []))}")
            print(f"   候选股数量: {len(institutional_result.get('top_candidates', []))}")
            if institutional_result.get('message'):
                print(f"   消息: {institutional_result['message']}")
        except Exception as e:
            print(f"   错误: {str(e)}")
        
        # 测试3: 中小票龙头股分析
        print("\n3. 测试中小票龙头股分析...")
        try:
            small_cap_result = perform_analysis('small_cap_leader', {
                'max_market_cap': 10000000000  # 100亿
            })
            print(f"   中小票龙头数量: {len(small_cap_result.get('small_cap_leaders', []))}")
            print(f"   详细分析数量: {len(small_cap_result.get('top_leaders', []))}")
            if small_cap_result.get('message'):
                print(f"   消息: {small_cap_result['message']}")
        except Exception as e:
            print(f"   错误: {str(e)}")
        
        # 测试4: 小票热门股分析
        print("\n4. 测试小票热门股分析...")
        try:
            hot_result = perform_analysis('small_cap_hot', {
                'max_market_cap': 5000000000  # 50亿
            })
            print(f"   小票热门股数量: {len(hot_result.get('small_cap_hot_stocks', []))}")
            print(f"   热门股详情数量: {len(hot_result.get('top_hot_stocks', []))}")
            if hot_result.get('message'):
                print(f"   消息: {hot_result['message']}")
        except Exception as e:
            print(f"   错误: {str(e)}")
        
        # 测试5: 低估股票分析
        print("\n5. 测试低估股票分析...")
        try:
            undervalued_result = perform_analysis('undervalued', {
                'pe_threshold': 15,
                'pb_threshold': 1.5
            })
            print(f"   低估股票数量: {len(undervalued_result.get('undervalued_stocks', []))}")
            print(f"   详细分析数量: {len(undervalued_result.get('detailed_analysis', []))}")
            if undervalued_result.get('message'):
                print(f"   消息: {undervalued_result['message']}")
        except Exception as e:
            print(f"   错误: {str(e)}")
        
        # 测试6: AI分析功能
        print("\n6. 测试AI股票分析...")
        try:
            ai_result = perform_analysis('ai_analysis', {
                'symbol': test_symbol,
                'type': 'comprehensive'
            })
            print(f"   AI分析结果长度: {len(ai_result.get('ai_analysis', '')) if ai_result.get('ai_analysis') else 0}")
            if ai_result.get('fallback'):
                print("   (使用模拟服务)")
        except Exception as e:
            print(f"   错误: {str(e)}")
        
        print("\n=== 股票分析功能测试完成 ===")

if __name__ == "__main__":
    test_stock_analysis()