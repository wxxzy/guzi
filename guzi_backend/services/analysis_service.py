# guzi_backend/services/analysis_service.py

from flask import current_app
from sqlalchemy import func
from ..database import db
from ..models import Stock
from .data_service import get_all_stocks # 可能会用到实时数据，但目前只获取基础列表
import akshare as ak
import pandas as pd

def identify_sector_leaders(industry_name: str):
    """
    识别指定行业内的龙一龙二股票。
    基于市值、涨跌幅和成交量进行综合评分。
    
    Args:
        industry_name (str): 行业名称。
        
    Returns:
        list: 包含龙一龙二股票信息的列表。
    """
    # 1. 从数据库获取指定行业的所有股票
    stocks_in_industry = Stock.query.filter_by(industry=industry_name).all()
    if not stocks_in_industry:
        return []

    stock_codes = [s.code for s in stocks_in_industry]

    # 2. 获取这些股票的实时市场数据
    # 注意：ak.stock_zh_a_spot_em() 之前遇到过连接问题，这里需要谨慎处理
    # 暂时使用一个更稳定的接口，或者假设能获取到数据
    try:
        # 尝试获取A股实时行情数据
        # 这是一个可能失败的接口，需要有容错机制
        realtime_data_df = ak.stock_zh_a_spot_em()
        # 过滤出当前行业股票的数据
        realtime_data_df = realtime_data_df[realtime_data_df['代码'].isin(stock_codes)]
        
        if realtime_data_df.empty:
            print(f"Warning: No real-time data found for industry {industry_name}. Using dummy data for scoring.")
            # 如果没有实时数据，则创建虚拟数据，避免程序崩溃
            realtime_data_df = pd.DataFrame({
                '代码': stock_codes,
                '最新价': [10.0] * len(stock_codes),
                '涨跌幅': [0.0] * len(stock_codes),
                '成交额': [10000000.0] * len(stock_codes),
                '总市值': [1000000000.0] * len(stock_codes),
            })

    except Exception as e:
        print(f"Error fetching real-time data for sector leaders: {e}. Using dummy data for scoring.")
        # 如果获取实时数据失败，则创建虚拟数据
        realtime_data_df = pd.DataFrame({
            '代码': stock_codes,
            '最新价': [10.0] * len(stock_codes),
            '涨跌幅': [0.0] * len(stock_codes),
            '成交额': [10000000.0] * len(stock_codes),
            '总市值': [1000000000.0] * len(stock_codes),
        })

    # 3. 合并数据库中的股票名称和实时数据
    merged_df = pd.merge(
        pd.DataFrame([{'code': s.code, 'name': s.name} for s in stocks_in_industry]),
        realtime_data_df,
        left_on='code',
        right_on='代码',
        how='left'
    )
    # 填充缺失的实时数据，避免评分时出错
    merged_df['总市值'] = merged_df['总市值'].fillna(0)
    merged_df['涨跌幅'] = merged_df['涨跌幅'].fillna(0)
    merged_df['成交额'] = merged_df['成交额'].fillna(0)

    # 4. 应用评分逻辑
    # 评分权重：市值(40%) + 涨跌幅(30%) + 成交额(30%)
    # 需要对数据进行归一化处理，避免量纲影响
    if merged_df.empty:
        return []

    # 归一化处理
    merged_df['市值_norm'] = (merged_df['总市值'] - merged_df['总市值'].min()) / (merged_df['总市值'].max() - merged_df['总市值'].min() + 1e-9)
    merged_df['涨跌幅_norm'] = (merged_df['涨跌幅'] - merged_df['涨跌幅'].min()) / (merged_df['涨跌幅'].max() - merged_df['涨跌幅'].min() + 1e-9)
    merged_df['成交额_norm'] = (merged_df['成交额'] - merged_df['成交额'].min()) / (merged_df['成交额'].max() - merged_df['成交额'].min() + 1e-9)

    # 计算综合评分
    merged_df['score'] = (
        merged_df['市值_norm'] * 0.4 +
        merged_df['涨跌幅_norm'] * 0.3 +
        merged_df['成交额_norm'] * 0.3
    )

    # 5. 排序并返回龙一龙二
    merged_df = merged_df.sort_values(by='score', ascending=False)
    
    leaders = []
    for _, row in merged_df.head(2).iterrows():
        leaders.append({
            'code': row['code'],
            'name': row['name'],
            'industry': industry_name,
            'score': round(row['score'], 2),
            'market_cap': row['总市值'],
            'change_percent': row['涨跌幅'],
            'volume_amount': row['成交额']
        })
    
    return leaders
