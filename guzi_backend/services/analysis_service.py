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

def analyze_institutional_holdings():
    """
    分析并识别机构重仓股。
    基于大市值、高流动性、价格稳定性等指标进行综合评分，模拟机构偏好。
    
    Returns:
        list: 包含机构偏好股票信息的列表。
    """
    # 1. 从数据库获取所有股票
    all_stocks = Stock.query.all()
    if not all_stocks:
        return []

    stock_codes = [s.code for s in all_stocks]

    # 2. 获取这些股票的实时市场数据
    try:
        realtime_data_df = ak.stock_zh_a_spot_em()
        realtime_data_df = realtime_data_df[realtime_data_df['代码'].isin(stock_codes)]

        if realtime_data_df.empty:
            print("Warning: No real-time data found for institutional analysis. Using dummy data.")
            realtime_data_df = pd.DataFrame({
                '代码': stock_codes,
                '最新价': [10.0] * len(stock_codes),
                '涨跌幅': [0.0] * len(stock_codes),
                '成交额': [10000000.0] * len(stock_codes),
                '总市值': [1000000000.0] * len(stock_codes),
            })

    except Exception as e:
        print(f"Error fetching real-time data for institutional analysis: {e}. Using dummy data.")
        realtime_data_df = pd.DataFrame({
            '代码': stock_codes,
            '最新价': [10.0] * len(stock_codes),
            '涨跌幅': [0.0] * len(stock_codes),
            '成交额': [10000000.0] * len(stock_codes),
            '总市值': [1000000000.0] * len(stock_codes),
        })

    # 3. 合并数据库中的股票名称和实时数据
    merged_df = pd.merge(
        pd.DataFrame([{'code': s.code, 'name': s.name, 'industry': s.industry} for s in all_stocks]),
        realtime_data_df,
        left_on='code',
        right_on='代码',
        how='left'
    )
    # 填充缺失的实时数据
    merged_df['总市值'] = merged_df['总市值'].fillna(0)
    merged_df['涨跌幅'] = merged_df['涨跌幅'].fillna(0)
    merged_df['成交额'] = merged_df['成交额'].fillna(0)

    if merged_df.empty:
        return []

    # 4. 应用评分逻辑
    # 机构偏好：大市值、高流动性、价格稳定性
    # 评分权重：市值(40%) + 成交额(30%) + 价格稳定性(30%)
    # 价格稳定性：涨跌幅绝对值越小越稳定，所以取其倒数或用 (1 - abs(涨跌幅)/max_abs_涨跌幅) 归一化

    # 归一化处理
    # 市值归一化
    merged_df['市值_norm'] = (merged_df['总市值'] - merged_df['总市值'].min()) / (merged_df['总市值'].max() - merged_df['总市值'].min() + 1e-9)
    # 成交额归一化
    merged_df['成交额_norm'] = (merged_df['成交额'] - merged_df['成交额'].min()) / (merged_df['成交额'].max() - merged_df['成交额'].min() + 1e-9)
    # 价格稳定性归一化 (涨跌幅绝对值越小，稳定性越高，得分越高)
    max_abs_change = merged_df['涨跌幅'].abs().max()
    if max_abs_change > 0:
        merged_df['稳定性_norm'] = 1 - (merged_df['涨跌幅'].abs() / max_abs_change)
    else:
        merged_df['稳定性_norm'] = 1.0 # 如果所有涨跌幅都为0，则都视为最稳定

    # 计算综合评分
    merged_df['institutional_score'] = (
        merged_df['市值_norm'] * 0.4 +
        merged_df['成交额_norm'] * 0.3 +
        merged_df['稳定性_norm'] * 0.3
    )

    # 5. 排序并返回前N名
    merged_df = merged_df.sort_values(by='institutional_score', ascending=False)
    
    top_institutional_stocks = []
    for _, row in merged_df.head(10).iterrows(): # 返回前10名作为示例
        top_institutional_stocks.append({
            'code': row['code'],
            'name': row['name'],
            'industry': row['industry'],
            'institutional_score': round(row['institutional_score'], 2),
            'market_cap': row['总市值'],
            'change_percent': row['涨跌幅'],
            'volume_amount': row['成交额']
        })
    
    return top_institutional_stocks

def identify_small_cap_leaders(market_cap_threshold: float = 500_000_000_000): # 5000亿作为中小市值上限示例
    """
    识别中小票龙头股。
    专注于小市值股票，结合动量、流动性等因素综合评估。
    
    Args:
        market_cap_threshold (float): 定义中小票的市值上限。
        
    Returns:
        list: 包含中小票龙头股信息的列表。
    """
    # 1. 从数据库获取所有股票
    all_stocks = Stock.query.all()
    if not all_stocks:
        return []

    stock_codes = [s.code for s in all_stocks]

    # 2. 获取这些股票的实时市场数据
    try:
        realtime_data_df = ak.stock_zh_a_spot_em()
        realtime_data_df = realtime_data_df[realtime_data_df['代码'].isin(stock_codes)]

        if realtime_data_df.empty:
            print("Warning: No real-time data found for small-cap analysis. Using dummy data.")
            realtime_data_df = pd.DataFrame({
                '代码': stock_codes,
                '最新价': [10.0] * len(stock_codes),
                '涨跌幅': [0.0] * len(stock_codes),
                '成交额': [10000000.0] * len(stock_codes),
                '总市值': [1000000000.0] * len(stock_codes),
            })

    except Exception as e:
        print(f"Error fetching real-time data for small-cap analysis: {e}. Using dummy data.")
        realtime_data_df = pd.DataFrame({
            '代码': stock_codes,
            '最新价': [10.0] * len(stock_codes),
            '涨跌幅': [0.0] * len(stock_codes),
            '成交额': [10000000.0] * len(stock_codes),
            '总市值': [1000000000.0] * len(stock_codes),
        })

    # 3. 合并数据库中的股票名称和实时数据
    merged_df = pd.merge(
        pd.DataFrame([{'code': s.code, 'name': s.name, 'industry': s.industry} for s in all_stocks]),
        realtime_data_df,
        left_on='code',
        right_on='代码',
        how='left'
    )
    # 填充缺失的实时数据
    merged_df['总市值'] = merged_df['总市值'].fillna(0)
    merged_df['涨跌幅'] = merged_df['涨跌幅'].fillna(0)
    merged_df['成交额'] = merged_df['成交额'].fillna(0)

    if merged_df.empty:
        return []

    # 4. 筛选中小票
    small_cap_df = merged_df[merged_df['总市值'] < market_cap_threshold]
    if small_cap_df.empty:
        return []

    # 5. 应用评分逻辑
    # 评分权重：市值(30%，市值越小越好) + 动量(40%，涨跌幅越大越好) + 流动性(30%，成交额越大越好)

    # 归一化处理
    # 市值归一化 (市值越小得分越高，所以用 (max - val) / (max - min) 归一化)
    min_market_cap = small_cap_df['总市值'].min()
    max_market_cap = small_cap_df['总市值'].max()
    if max_market_cap - min_market_cap > 1e-9:
        small_cap_df['市值_norm'] = (max_market_cap - small_cap_df['总市值']) / (max_market_cap - min_market_cap)
    else:
        small_cap_df['市值_norm'] = 0.5 # 如果市值都一样，给个中等分

    # 动量归一化 (涨跌幅越大得分越高)
    min_change = small_cap_df['涨跌幅'].min()
    max_change = small_cap_df['涨跌幅'].max()
    if max_change - min_change > 1e-9:
        small_cap_df['涨跌幅_norm'] = (small_cap_df['涨跌幅'] - min_change) / (max_change - min_change)
    else:
        small_cap_df['涨跌幅_norm'] = 0.5

    # 流动性归一化 (成交额越大得分越高)
    min_volume = small_cap_df['成交额'].min()
    max_volume = small_cap_df['成交额'].max()
    if max_volume - min_volume > 1e-9:
        small_cap_df['成交额_norm'] = (small_cap_df['成交额'] - min_volume) / (max_volume - min_volume)
    else:
        small_cap_df['成交额_norm'] = 0.5

    # 计算综合评分
    small_cap_df['small_cap_score'] = (
        small_cap_df['市值_norm'] * 0.3 +
        small_cap_df['涨跌幅_norm'] * 0.4 +
        small_cap_df['成交额_norm'] * 0.3
    )

    # 6. 排序并返回前N名
    small_cap_df = small_cap_df.sort_values(by='small_cap_score', ascending=False)
    
    top_small_cap_stocks = []
    for _, row in small_cap_df.head(10).iterrows(): # 返回前10名作为示例
        top_small_cap_stocks.append({
            'code': row['code'],
            'name': row['name'],
            'industry': row['industry'],
            'small_cap_score': round(row['small_cap_score'], 2),
            'market_cap': row['总市值'],
            'change_percent': row['涨跌幅'],
            'volume_amount': row['成交额']
        })
    
    return top_small_cap_stocks

def identify_undervalued_stocks():
    """
    识别低估股票。
    基于PE、PB等估值指标进行综合分析。
    
    Returns:
        list: 包含低估股票信息的列表。
    """
    # 1. 从数据库获取所有股票
    all_stocks = Stock.query.all()
    if not all_stocks:
        return []

    stock_codes = [s.code for s in all_stocks]

    # 2. 获取这些股票的估值数据 (PE, PB)
    try:
        # ak.stock_a_pe_pb_em() 提供了A股的市盈率和市净率
        valuation_df = ak.stock_a_pe_pb_em()
        valuation_df = valuation_df[valuation_df['股票代码'].isin(stock_codes)]

        if valuation_df.empty:
            print("Warning: No valuation data found. Using dummy data.")
            valuation_df = pd.DataFrame({
                '股票代码': stock_codes,
                '市盈率': [20.0] * len(stock_codes),
                '市净率': [2.0] * len(stock_codes),
            })

    except Exception as e:
        print(f"Error fetching valuation data: {e}. Using dummy data.")
        valuation_df = pd.DataFrame({
            '股票代码': stock_codes,
            '市盈率': [20.0] * len(stock_codes),
            '市净率': [2.0] * len(stock_codes),
        })

    # 3. 合并数据库中的股票名称、行业和估值数据
    merged_df = pd.merge(
        pd.DataFrame([{'code': s.code, 'name': s.name, 'industry': s.industry} for s in all_stocks]),
        valuation_df,
        left_on='code',
        right_on='股票代码',
        how='left'
    )
    # 填充缺失的估值数据
    merged_df['市盈率'] = merged_df['市盈率'].fillna(9999) # 缺失值设为高估值
    merged_df['市净率'] = merged_df['市净率'].fillna(9999) # 缺失值设为高估值

    if merged_df.empty:
        return []

    # 过滤掉非正估值 (PE/PB < 0)
    merged_df = merged_df[(merged_df['市盈率'] > 0) & (merged_df['市净率'] > 0)]
    if merged_df.empty:
        return []

    # 4. 应用评分逻辑
    # 评分权重：PE(50%) + PB(50%)
    # PE和PB越低越好，所以归一化时取倒数或用 (max - val) / (max - min)

    # 归一化处理
    # PE归一化 (PE越低得分越高)
    min_pe = merged_df['市盈率'].min()
    max_pe = merged_df['市盈率'].max()
    if max_pe - min_pe > 1e-9:
        merged_df['PE_norm'] = (max_pe - merged_df['市盈率']) / (max_pe - min_pe)
    else:
        merged_df['PE_norm'] = 0.5

    # PB归一化 (PB越低得分越高)
    min_pb = merged_df['市净率'].min()
    max_pb = merged_df['市净率'].max()
    if max_pb - min_pb > 1e-9:
        merged_df['PB_norm'] = (max_pb - merged_df['市净率']) / (max_pb - min_pb)
    else:
        merged_df['PB_norm'] = 0.5

    # 计算综合评分
    merged_df['undervalued_score'] = (
        merged_df['PE_norm'] * 0.5 +
        merged_df['PB_norm'] * 0.5
    )

    # 5. 排序并返回前N名
    merged_df = merged_df.sort_values(by='undervalued_score', ascending=False)
    
    top_undervalued_stocks = []
    for _, row in merged_df.head(10).iterrows(): # 返回前10名作为示例
        top_undervalued_stocks.append({
            'code': row['code'],
            'name': row['name'],
            'industry': row['industry'],
            'undervalued_score': round(row['undervalued_score'], 2),
            'pe': row['市盈率'],
            'pb': row['市净率']
        })
    
    return top_undervalued_stocks

def get_comprehensive_score():
    """
    计算所有股票的综合评分。
    基于技术面(30%) + 基本面(40%) + 估值面(30%)进行综合评分。
    
    Returns:
        list: 包含所有股票及其综合评分的列表。
    """
    # 1. 从数据库获取所有股票
    all_stocks = Stock.query.all()
    if not all_stocks:
        return []

    stock_codes = [s.code for s in all_stocks]

    # 2. 获取实时市场数据 (市值, 涨跌幅)
    try:
        realtime_data_df = ak.stock_zh_a_spot_em()
        realtime_data_df = realtime_data_df[realtime_data_df['代码'].isin(stock_codes)]
    except Exception as e:
        print(f"Error fetching real-time data for comprehensive score: {e}. Using dummy data.")
        realtime_data_df = pd.DataFrame({
            '代码': stock_codes,
            '涨跌幅': [0.0] * len(stock_codes),
            '总市值': [1000000000.0] * len(stock_codes),
        })

    # 3. 获取估值数据 (PE, PB)
    try:
        valuation_df = ak.stock_a_pe_pb_em()
        valuation_df = valuation_df[valuation_df['股票代码'].isin(stock_codes)]
    except Exception as e:
        print(f"Error fetching valuation data for comprehensive score: {e}. Using dummy data.")
        valuation_df = pd.DataFrame({
            '股票代码': stock_codes,
            '市盈率': [20.0] * len(stock_codes),
            '市净率': [2.0] * len(stock_codes),
        })

    # 4. 合并所有数据
    merged_df = pd.merge(
        pd.DataFrame([{'code': s.code, 'name': s.name, 'industry': s.industry} for s in all_stocks]),
        realtime_data_df,
        left_on='code',
        right_on='代码',
        how='left'
    )
    merged_df = pd.merge(
        merged_df,
        valuation_df,
        left_on='code',
        right_on='股票代码',
        how='left'
    )

    # 填充缺失数据
    merged_df['总市值'] = merged_df['总市值'].fillna(0)
    merged_df['涨跌幅'] = merged_df['涨跌幅'].fillna(0)
    merged_df['市盈率'] = merged_df['市盈率'].fillna(9999)
    merged_df['市净率'] = merged_df['市净率'].fillna(9999)

    if merged_df.empty:
        return []

    # 5. 应用评分逻辑
    # 技术面(30%) + 基本面(40%) + 估值面(30%)

    # 归一化处理
    # 技术面 (涨跌幅，越高越好)
    min_change = merged_df['涨跌幅'].min()
    max_change = merged_df['涨跌幅'].max()
    if max_change - min_change > 1e-9:
        merged_df['tech_norm'] = (merged_df['涨跌幅'] - min_change) / (max_change - min_change)
    else:
        merged_df['tech_norm'] = 0.5

    # 基本面 (总市值，越高越好)
    min_market_cap = merged_df['总市值'].min()
    max_market_cap = merged_df['总市值'].max()
    if max_market_cap - min_market_cap > 1e-9:
        merged_df['fund_norm'] = (merged_df['总市值'] - min_market_cap) / (max_market_cap - min_market_cap)
    else:
        merged_df['fund_norm'] = 0.5

    # 估值面 (PE, PB，越低越好)
    # 过滤掉非正估值
    valid_valuation_df = merged_df[(merged_df['市盈率'] > 0) & (merged_df['市净率'] > 0)]
    
    if not valid_valuation_df.empty:
        min_pe = valid_valuation_df['市盈率'].min()
        max_pe = valid_valuation_df['市盈率'].max()
        if max_pe - min_pe > 1e-9:
            merged_df['PE_norm'] = (max_pe - merged_df['市盈率']) / (max_pe - min_pe)
        else:
            merged_df['PE_norm'] = 0.5

        min_pb = valid_valuation_df['市净率'].min()
        max_pb = valid_valuation_df['市净率'].max()
        if max_pb - min_pb > 1e-9:
            merged_df['PB_norm'] = (max_pb - merged_df['市净率']) / (max_pb - min_pb)
        else:
            merged_df['PB_norm'] = 0.5

        # 估值综合分
        merged_df['val_norm'] = (merged_df['PE_norm'] + merged_df['PB_norm']) / 2
    else:
        merged_df['val_norm'] = 0.5 # 如果没有有效估值数据，给个中等分

    # 计算综合评分
    merged_df['comprehensive_score'] = (
        merged_df['tech_norm'] * 0.3 +
        merged_df['fund_norm'] * 0.4 +
        merged_df['val_norm'] * 0.3
    )

    # 6. 排序并返回
    merged_df = merged_df.sort_values(by='comprehensive_score', ascending=False)
    
    scored_stocks = []
    for _, row in merged_df.head(20).iterrows(): # 返回前20名作为示例
        scored_stocks.append({
            'code': row['code'],
            'name': row['name'],
            'industry': row['industry'],
            'comprehensive_score': round(row['comprehensive_score'], 2),
            'market_cap': row['总市值'],
            'change_percent': row['涨跌幅'],
            'pe': row['市盈率'],
            'pb': row['市净率']
        })
    
    return scored_stocks
