"""
股票综合评分系统
"""
from models import Stock, StockData
from data_source.data_fetcher import fetch_stock_data, fetch_financial_indicators
from datetime import datetime, timedelta
import pandas as pd
import numpy as np

def calculate_technical_score(symbol):
    """
    计算技术面评分
    :param symbol: 股票代码
    :return: 技术面评分 (0-100)
    """
    # 获取60天的历史数据
    end_date = datetime.now().strftime('%Y%m%d')
    start_date = (datetime.now() - timedelta(days=70)).strftime('%Y%m%d')  # 多取10天以防周末
    stock_data = fetch_stock_data(symbol, start_date, end_date)
    
    if stock_data.empty or len(stock_data) < 20:
        return 50  # 数据不足时返回中性评分
    
    # 确保数据按日期升序排列
    stock_data = stock_data.sort_values('date')
    prices = stock_data['close_price'].values
    volumes = stock_data['volume'].values if 'volume' in stock_data.columns else np.ones(len(prices)) * 1000000
    
    # 计算技术指标
    # 1. 移动平均线指标
    ma5 = np.mean(prices[-5:]) if len(prices) >= 5 else prices[-1]
    ma20 = np.mean(prices[-20:]) if len(prices) >= 20 else prices[-1]
    current_price = prices[-1]
    
    # MA5相对于MA20的位置评分 (趋势)
    trend_score = 0
    if ma20 != 0:
        ma_position = (ma5 - ma20) / ma20 * 100
        trend_score = max(min(ma_position * 2, 30), -30) + 50  # 映射到20-80分
    
    # 2. 价格动量评分
    if len(prices) >= 10:
        momentum_10 = (prices[-1] - prices[-11]) / prices[-11] * 100
        momentum_score = max(min(momentum_10 * 2, 30), -30) + 50
    else:
        momentum_score = 50
    
    # 3. 价格波动率评分 (稳定性)
    if len(prices) >= 20:
        volatility = np.std(prices[-20:]) / np.mean(prices[-20:])
        # 波动率越低越稳定，给予更高评分
        volatility_score = max(70 - volatility * 1000, 10)  # 波动越小分数越高
    else:
        volatility_score = 50
    
    # 4. 成交量评分 (活跃度)
    if len(volumes) >= 10:
        avg_vol_10 = np.mean(volumes[-10:])
        avg_vol_30 = np.mean(volumes) if len(volumes) >= 30 else avg_vol_10
        if avg_vol_30 > 0:
            volume_score = min(avg_vol_10 / avg_vol_30 * 30, 60)  # 活跃度评分
        else:
            volume_score = 30
    else:
        volume_score = 30
    
    # 综合技术评分 (趋势30% + 动量25% + 稳定性25% + 活跃度20%)
    tech_score = (trend_score * 0.3 + momentum_score * 0.25 + 
                  volatility_score * 0.25 + volume_score * 0.2)
    
    return round(max(min(tech_score, 100), 0), 2)

def calculate_fundamental_score(symbol):
    """
    计算基本面评分
    :param symbol: 股票代码
    :return: 基本面评分 (0-100)
    """
    # 从数据库获取股票信息
    stock = Stock.query.filter_by(symbol=symbol).first()
    if not stock:
        return 50
    
    # 获取财务数据
    financial_data = fetch_financial_indicators(symbol)
    
    # 基本面评分计算
    # 使用数据库中存储的基本财务指标
    pe_ratio = stock.pe_ratio or 0
    pb_ratio = stock.pb_ratio or 0
    
    # 如果有从财务数据API获取到的数据，则使用
    # 但目前我们的数据库结构和API可能不完全匹配，这里用默认值
    roe = 0.1  # 示例值，实际应从财务数据获取
    debt_ratio = 0.4  # 示例值，实际应从财务数据获取
    revenue_growth = 0.1  # 示例值，实际应从财务数据获取
    
    # PE评分 (越低越好，但不能为负或过低)
    if pe_ratio > 0 and pe_ratio < 100:
        pe_score = max(80 - pe_ratio * 2, 10)  # PE在40以下为高分
    else:
        pe_score = 50  # PE无效时的中性分
    
    # PB评分 (越低越好，但不能为负)
    if pb_ratio > 0 and pb_ratio < 10:
        pb_score = max(90 - pb_ratio * 8, 10)
    else:
        pb_score = 50  # PB无效时的中性分
    
    # ROE评分 (越高越好，但不超高)
    roe_score = min(roe * 200, 90) if roe >= 0 else 10
    
    # 负债率评分 (越低越好)
    debt_score = max(90 - debt_ratio * 100, 10) if debt_ratio >= 0 else 10
    
    # 收入增长率评分 (越高越好)
    growth_score = min(revenue_growth * 200, 90) if revenue_growth >= 0 else 10
    
    # 综合基本面评分 (PE 25% + PB 25% + ROE 20% + 负债率 15% + 增长 15%)
    fundamental_score = (pe_score * 0.25 + pb_score * 0.25 + 
                        roe_score * 0.2 + debt_score * 0.15 + 
                        growth_score * 0.15)
    
    return round(max(min(fundamental_score, 100), 0), 2)

def calculate_valuation_score(symbol):
    """
    计算估值面评分
    :param symbol: 股票代码
    :return: 估值面评分 (0-100) 
    """
    stock = Stock.query.filter_by(symbol=symbol).first()
    if not stock:
        return 50
    
    pe_ratio = stock.pe_ratio
    pb_ratio = stock.pb_ratio
    
    # 获取行业平均估值作为参考
    industry_pe_avg = 18  # 示例行业平均PE，实际应从行业数据获取
    industry_pb_avg = 1.8  # 示例行业平均PB，实际应从行业数据获取
    
    # 估值评分计算 (越低越被低估，分数越高)
    if pe_ratio and pe_ratio > 0:
        # 如果低于行业平均，评分更高
        pe_valuation_score = max(min((industry_pe_avg - pe_ratio) / industry_pe_avg * 50 + 50, 90), 10)
    else:
        pe_valuation_score = 50
    
    if pb_ratio and pb_ratio > 0:
        pb_valuation_score = max(min((industry_pb_avg - pb_ratio) / industry_pb_avg * 50 + 50, 90), 10)
    else:
        pb_valuation_score = 50
    
    # 综合估值评分
    valuation_score = (pe_valuation_score * 0.6 + pb_valuation_score * 0.4)
    
    return round(max(min(valuation_score, 100), 0), 2)

def calculate_comprehensive_score(symbol):
    """
    计算综合评分
    :param symbol: 股票代码
    :return: 综合评分详情
    """
    tech_score = calculate_technical_score(symbol)
    fundamental_score = calculate_fundamental_score(symbol)
    valuation_score = calculate_valuation_score(symbol)
    
    # 综合评分 (技术面30% + 基本面40% + 估值面30%)
    total_score = tech_score * 0.3 + fundamental_score * 0.4 + valuation_score * 0.3
    
    return {
        'symbol': symbol,
        'technical_score': tech_score,
        'fundamental_score': fundamental_score,
        'valuation_score': valuation_score,
        'comprehensive_score': round(total_score, 2),
        'rating': get_rating_from_score(total_score)
    }

def get_rating_from_score(score):
    """
    根据分数返回评级
    :param score: 综合评分
    :return: 评级
    """
    if score >= 80:
        return '强烈推荐'
    elif score >= 70:
        return '推荐'
    elif score >= 60:
        return '谨慎推荐'
    elif score >= 40:
        return '中性'
    else:
        return '回避'

def rank_stocks_by_comprehensive_score(limit=20):
    """
    按综合评分对股票进行排名
    :param limit: 返回前N只股票
    :return: 排名结果
    """
    # 获取所有股票
    all_stocks = Stock.query.all()
    
    ranked_list = []
    for stock in all_stocks:
        score_detail = calculate_comprehensive_score(stock.symbol)
        ranked_list.append(score_detail)
    
    # 按综合评分排序
    ranked_list.sort(key=lambda x: x['comprehensive_score'], reverse=True)
    
    return {
        'timestamp': datetime.now().isoformat(),
        'rankings': ranked_list[:limit],
        'total_analyzed': len(ranked_list)
    }