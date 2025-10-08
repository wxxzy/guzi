"""
测试数据源功能的脚本
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import create_app
from models import db, Stock
from data_source.data_fetcher import (
    fetch_stock_data, 
    fetch_stock_info, 
    sync_historical_data,
    get_market_data_summary
)
from datetime import datetime, timedelta

def test_data_source():
    app = create_app()
    
    with app.app_context():
        print("=== 测试数据源功能 ===")
        
        # 测试1: 获取股票列表
        print("\n1. 测试获取股票列表...")
        stocks = Stock.query.limit(5).all()
        print(f"获取到 {len(stocks)} 只股票:")
        for stock in stocks:
            print(f"  - {stock.symbol}: {stock.name} ({stock.industry})")
        
        # 测试2: 获取特定股票信息
        print("\n2. 测试获取特定股票信息...")
        if stocks:
            test_symbol = stocks[0].symbol
            stock_info = fetch_stock_info(test_symbol)
            if stock_info:
                print(f"股票 {test_symbol} 信息:")
                for key, value in stock_info.items():
                    print(f"  {key}: {value}")
            else:
                print(f"未获取到股票 {test_symbol} 的信息")
        
        # 测试3: 获取历史数据
        print("\n3. 测试获取历史数据...")
        if stocks:
            test_symbol = stocks[0].symbol
            end_date = datetime.now().strftime('%Y%m%d')
            start_date = (datetime.now() - timedelta(days=30)).strftime('%Y%m%d')
            stock_data = fetch_stock_data(test_symbol, start_date, end_date)
            if not stock_data.empty:
                print(f"获取到股票 {test_symbol} 最近30天的 {len(stock_data)} 条历史数据")
                print("最近5天数据:")
                for i, (_, row) in enumerate(stock_data.tail(5).iterrows()):
                    print(f"  {row['date']}: 开 {row['open_price']}, 收 {row['close_price']}, 量 {row['volume']}")
            else:
                print(f"未获取到股票 {test_symbol} 的历史数据")
        
        # 测试4: 同步历史数据
        print("\n4. 测试同步历史数据...")
        if stocks:
            test_symbol = stocks[0].symbol
            sync_result = sync_historical_data(test_symbol, days=7)  # 只同步最近7天
            print(f"历史数据同步结果: {sync_result}")
        
        # 测试5: 获取市场整体数据
        print("\n5. 测试获取市场整体数据...")
        market_summary = get_market_data_summary()
        if market_summary:
            print("市场整体数据:")
            for key, value in market_summary.items():
                print(f"  {key}: {value}")
        else:
            print("未获取到市场整体数据")
        
        print("\n=== 数据源功能测试完成 ===")

if __name__ == "__main__":
    test_data_source()