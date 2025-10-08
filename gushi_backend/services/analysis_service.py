from models import Stock, StockData, AnalysisResult
from ai_services.ai_manager import ai_manager
from ai_services.mock_ai_service import get_ai_response_with_fallback
from data_source.data_fetcher import fetch_stock_data, fetch_stock_info, fetch_financial_indicators
from services.scoring_service import calculate_comprehensive_score, rank_stocks_by_comprehensive_score
from datetime import datetime
import json

def perform_analysis(analysis_type, params):
    """
    执行股票分析
    :param analysis_type: 分析类型
    :param params: 分析参数
    :return: 分析结果
    """
    print(f"DEBUG: perform_analysis called with analysis_type: {analysis_type}")
    if analysis_type == 'dragon':
        print(f"DEBUG: calling analyze_sector_dragons with sector: {params.get('sector', '')}")
        return analyze_sector_dragons(params.get('sector', ''))
    elif analysis_type == 'institutional':
        return analyze_institutional_stocks(params.get('filters', {}))
    elif analysis_type == 'small_cap_leader':
        return analyze_small_cap_leaders(params.get('max_market_cap', 10000000000))
    elif analysis_type == 'small_cap_hot':
        return analyze_small_cap_hot_stocks(params.get('max_market_cap', 5000000000))
    elif analysis_type == 'undervalued':
        return analyze_undervalued_stocks(params)
    elif analysis_type == 'market_trend':
        return analyze_market_trends()
    elif analysis_type == 'comprehensive_score':
        return get_comprehensive_score(params.get('symbol', ''))
    elif analysis_type == 'stock_ranking':
        return get_stock_rankings(params.get('limit', 20))
    elif analysis_type == 'natural_language_query':
        return process_natural_language_query(params.get('query', ''), params.get('user_context', {}))
    elif analysis_type == 'personalized_recommendation':
        return generate_personalized_recommendation(params.get('user_profile', {}))
    elif analysis_type == 'sentiment_analysis':
        return perform_sentiment_analysis(params.get('text', ''))
    elif analysis_type == 'ai_analysis':
        return ai_stock_analysis(params.get('symbol'), params.get('type', 'comprehensive'))
    else:
        raise ValueError(f"未知的分析类型: {analysis_type}")

def process_natural_language_query(query, user_context):
    """处理自然语言查询"""
    try:
        result = ai_manager.process_natural_language_query(query, user_context)
        
        # 保存分析结果到数据库
        save_analysis_result(None, 'natural_language_query', json.dumps(result, ensure_ascii=False), 'ai_model')
        
        return result
    except Exception as e:
        error_result = {
            'error': str(e),
            'timestamp': datetime.now().isoformat()
        }
        return error_result

def generate_personalized_recommendation(user_profile):
    """生成个性化推荐"""
    try:
        result = ai_manager.generate_personalized_recommendation(user_profile)
        
        # 保存分析结果到数据库
        save_analysis_result(None, 'personalized_recommendation', json.dumps(result, ensure_ascii=False), 'ai_model')
        
        return result
    except Exception as e:
        error_result = {
            'error': str(e),
            'timestamp': datetime.now().isoformat()
        }
        return error_result

def perform_sentiment_analysis(text):
    """执行情绪分析"""
    try:
        result = ai_manager.sentiment_analysis(text)
        
        # 保存分析结果到数据库
        save_analysis_result(None, 'sentiment_analysis', json.dumps(result, ensure_ascii=False), 'ai_model')
        
        return result
    except Exception as e:
        error_result = {
            'error': str(e),
            'timestamp': datetime.now().isoformat()
        }
        return error_result

def get_comprehensive_score(symbol):
    """获取股票综合评分"""
    if not symbol:
        raise ValueError("股票代码不能为空")
    
    try:
        score_result = calculate_comprehensive_score(symbol)
        
        result = {
            'symbol': symbol,
            'comprehensive_analysis': score_result,
            'timestamp': datetime.now().isoformat()
        }
        
        # 保存分析结果到数据库
        save_analysis_result(symbol, 'comprehensive_score', json.dumps(result, ensure_ascii=False), 'scoring_algorithm')
        
        return result
    except Exception as e:
        error_result = {
            'symbol': symbol,
            'error': str(e),
            'timestamp': datetime.now().isoformat()
        }
        return error_result

def get_stock_rankings(limit=20):
    """获取股票综合评分排名"""
    try:
        ranking_result = rank_stocks_by_comprehensive_score(limit)
        
        result = {
            'rankings': ranking_result,
            'timestamp': datetime.now().isoformat()
        }
        
        # 保存分析结果到数据库
        save_analysis_result(None, 'stock_ranking', json.dumps(result, ensure_ascii=False), 'scoring_algorithm')
        
        return result
    except Exception as e:
        error_result = {
            'error': str(e),
            'timestamp': datetime.now().isoformat()
        }
        return error_result

def analyze_sector_dragons_realtime(sector, task_id, task_manager, limit=None):
    """实时分析板块龙一龙二，支持进度报告"""
    from data_source.data_fetcher import fetch_stock_data
    from datetime import timedelta
    
    # 添加调试信息
    print(f"DEBUG: analyze_sector_dragons_realtime called - sector={sector}, task_id={task_id}, task_manager={type(task_manager)}, limit={limit}")
    
    # 断言确保task_manager不是None
    assert task_manager is not None, "task_manager不能为None"
    
    # 如果没有指定行业，使用所有股票
    if sector:
        stocks = Stock.query.filter(Stock.industry.like(f'%{sector}%')).all()
    else:
        # 限制股票数量以提高性能，优先选择有市值信息的股票
        query = Stock.query
        if limit is None:
            limit = 100  # 默认限制为100只股票
        
        # 优先选择有市值数据的股票，如果没有市值则随机选择
        stocks_with_market_cap = query.filter(Stock.market_cap.isnot(None)).order_by(Stock.market_cap.desc()).limit(limit).all()
        stocks_without_market_cap = []
        
        # 如果有市值的股票不够，补充没有市值的股票
        if len(stocks_with_market_cap) < limit:
            remaining_count = limit - len(stocks_with_market_cap)
            stocks_without_market_cap = query.filter(Stock.market_cap.is_(None)).limit(remaining_count).all()
        
        stocks = stocks_with_market_cap + stocks_without_market_cap
    
    if not stocks:
        return {
            'sector': sector,
            'timestamp': datetime.now().isoformat(),
            'dragons': [],
            'top_stocks': [],
            'message': '未找到相关股票数据'
        }
    
    # 更新总任务数
    total_stocks = len(stocks)
    print(f"DEBUG: Updating task progress with task_manager={type(task_manager)}, task_id={task_id}")
    task_manager.update_task_progress(task_id, 0, f"开始分析 {total_stocks} 只股票", None)
    
    # 计算每只股票的综合评分（考虑市值、涨幅、成交量等因素）
    ranked_stocks = []
    for i, stock in enumerate(stocks):
        # 更新进度
        progress = int((i / total_stocks) * 80)  # 分析阶段占80%的进度
        task_manager.update_task_progress(
            task_id, 
            progress, 
            f"正在分析股票 {i+1}/{total_stocks}", 
            f"{stock.name}({stock.symbol})"
        )
        
        # 获取近期数据以计算涨幅和成交量
        # 获取最近10个交易日的数据
        end_date = datetime.now().strftime('%Y%m%d')
        start_date = (datetime.now() - timedelta(days=15)).strftime('%Y%m%d')  # 多几天以防周末
        stock_data = fetch_stock_data(stock.symbol, start_date, end_date)
        
        if not stock_data.empty and len(stock_data) >= 2:
            # 计算10日涨幅
            recent_price = stock_data.iloc[-1]['close_price']
            prev_price = stock_data.iloc[0]['close_price']
            if prev_price and prev_price != 0:
                price_change_pct = (recent_price - prev_price) / prev_price * 100
            else:
                price_change_pct = 0
            
            # 计算平均成交量
            avg_volume = stock_data['volume'].mean() if 'volume' in stock_data.columns else 0
        else:
            price_change_pct = 0
            avg_volume = 0
        
        # 计算综合评分 (市值权重30%, 涨幅权重40%, 成交量权重30%)
        market_cap_score = min((stock.market_cap or 0) / 1000000000, 10) if stock.market_cap else 0  # 市值评分，最高10分
        price_score = max(min(price_change_pct, 20), -20) / 2  # 涨幅评分，限制在-10到10之间
        volume_score = min(avg_volume / 10000000, 10) if avg_volume else 0  # 成交量评分，最高10分
        
        # 归一化到0-100分制
        total_score = (market_cap_score * 0.3 + price_score * 0.4 + volume_score * 0.3) * 10
        
        ranked_stocks.append({
            'stock': stock.to_dict(),
            'score': total_score,
            'price_change_pct': price_change_pct,
            'avg_volume': avg_volume
        })
    
    # 更新进度到排序阶段
    task_manager.update_task_progress(task_id, 85, "正在排序股票", "排序中...")
    
    # 按综合评分排序
    ranked_stocks.sort(key=lambda x: x['score'], reverse=True)
    
    # 更新进度到生成结果阶段
    task_manager.update_task_progress(task_id, 95, "正在生成分析结果", "收尾工作...")
    
    # 获取龙一龙二（前2名）
    dragons = [item['stock'] for item in ranked_stocks[:2]]
    
    result = {
        'sector': sector,
        'timestamp': datetime.now().isoformat(),
        'dragons': dragons,
        'top_stocks': [item['stock'] for item in ranked_stocks[:10]],  # 前10名
        'all_ranked': [
            {
                'stock': item['stock'],
                'score': round(item['score'], 2),
                'price_change_pct': round(item['price_change_pct'], 2),
                'avg_volume': int(item['avg_volume']) if item['avg_volume'] else 0
            }
            for item in ranked_stocks[:20]  # 前20名详细信息
        ],
        'total_analyzed': total_stocks  # 添加分析总数
    }
    
    # 保存分析结果到数据库
    save_analysis_result(None, 'dragon', json.dumps(result, ensure_ascii=False), 'internal_algorithm')
    
    return result

def analyze_sector_dragons(sector, limit=None):
    """分析板块龙一龙二（同步版本）"""
    from data_source.data_fetcher import fetch_stock_data
    from datetime import timedelta
    
    # 如果没有指定行业，使用所有股票
    if sector:
        stocks = Stock.query.filter(Stock.industry.like(f'%{sector}%')).all()
    else:
        # 限制股票数量以提高性能，优先选择有市值信息的股票
        query = Stock.query
        if limit is None:
            limit = 100  # 默认限制为100只股票
        
        # 优先选择有市值数据的股票，如果没有市值则随机选择
        stocks_with_market_cap = query.filter(Stock.market_cap.isnot(None)).order_by(Stock.market_cap.desc()).limit(limit).all()
        stocks_without_market_cap = []
        
        # 如果有市值的股票不够，补充没有市值的股票
        if len(stocks_with_market_cap) < limit:
            remaining_count = limit - len(stocks_with_market_cap)
            stocks_without_market_cap = query.filter(Stock.market_cap.is_(None)).limit(remaining_count).all()
        
        stocks = stocks_with_market_cap + stocks_without_market_cap
    
    if not stocks:
        return {
            'sector': sector,
            'timestamp': datetime.now().isoformat(),
            'dragons': [],
            'top_stocks': [],
            'message': '未找到相关股票数据'
        }
    
    # 计算每只股票的综合评分（考虑市值、涨幅、成交量等因素）
    ranked_stocks = []
    for stock in stocks:
        # 获取近期数据以计算涨幅和成交量
        # 获取最近10个交易日的数据
        end_date = datetime.now().strftime('%Y%m%d')
        start_date = (datetime.now() - timedelta(days=15)).strftime('%Y%m%d')  # 多几天以防周末
        stock_data = fetch_stock_data(stock.symbol, start_date, end_date)
        
        if not stock_data.empty and len(stock_data) >= 2:
            # 计算10日涨幅
            recent_price = stock_data.iloc[-1]['close_price']
            prev_price = stock_data.iloc[0]['close_price']
            if prev_price and prev_price != 0:
                price_change_pct = (recent_price - prev_price) / prev_price * 100
            else:
                price_change_pct = 0
            
            # 计算平均成交量
            avg_volume = stock_data['volume'].mean() if 'volume' in stock_data.columns else 0
        else:
            price_change_pct = 0
            avg_volume = 0
        
        # 计算综合评分 (市值权重30%, 涨幅权重40%, 成交量权重30%)
        market_cap_score = min((stock.market_cap or 0) / 1000000000, 10) if stock.market_cap else 0  # 市值评分，最高10分
        price_score = max(min(price_change_pct, 20), -20) / 2  # 涨幅评分，限制在-10到10之间
        volume_score = min(avg_volume / 10000000, 10) if avg_volume else 0  # 成交量评分，最高10分
        
        # 归一化到0-100分制
        total_score = (market_cap_score * 0.3 + price_score * 0.4 + volume_score * 0.3) * 10
        
        ranked_stocks.append({
            'stock': stock.to_dict(),
            'score': total_score,
            'price_change_pct': price_change_pct,
            'avg_volume': avg_volume
        })
    
    # 按综合评分排序
    ranked_stocks.sort(key=lambda x: x['score'], reverse=True)
    
    # 获取龙一龙二（前2名）
    dragons = [item['stock'] for item in ranked_stocks[:2]]
    
    result = {
        'sector': sector,
        'timestamp': datetime.now().isoformat(),
        'dragons': dragons,
        'top_stocks': [item['stock'] for item in ranked_stocks[:10]],  # 前10名
        'all_ranked': [
            {
                'stock': item['stock'],
                'score': round(item['score'], 2),
                'price_change_pct': round(item['price_change_pct'], 2),
                'avg_volume': int(item['avg_volume']) if item['avg_volume'] else 0
            }
            for item in ranked_stocks[:20]  # 前20名详细信息
        ]
    }
    
    # 保存分析结果到数据库
    save_analysis_result(None, 'dragon', json.dumps(result, ensure_ascii=False), 'internal_algorithm')
    
    return result

def analyze_institutional_stocks(filters):
    """分析机构重仓股"""
    # 模拟机构持仓数据分析
    # 在实际应用中，这里应该从专门的机构持仓数据源获取数据
    # 目前基于一些指标来估算机构可能重仓的股票
    
    # 获取筛选条件
    min_market_cap = filters.get('min_market_cap', 5000000000)  # 默认50亿以上，机构更偏好大市值
    min_float_market_cap = filters.get('min_float_market_cap', 2000000000)  # 流通市值要求
    min_roe = filters.get('min_roe', 0.08)  # 最低ROE要求
    max_debt_ratio = filters.get('max_debt_ratio', 0.6)  # 最大负债率
    
    # 构建查询条件
    query = Stock.query
    
    # 应用筛选条件
    if min_market_cap:
        query = query.filter(Stock.market_cap >= min_market_cap)
    if min_roe:
        query = query.filter(Stock.pe_ratio != None)  # 确保有财务数据
    # 注意：数据库中目前可能没有ROE和负债率字段，这里只做示意
    
    # 获取股票列表
    stocks = query.limit(50).all()  # 限制数量以提高性能
    
    if not stocks:
        return {
            'filters': filters,
            'timestamp': datetime.now().isoformat(),
            'institutional_heavy_holding': [],
            'message': '未找到符合条件的股票'
        }
    
    # 为每只股票计算机构持仓概率评分
    # 基于市值、流动性、稳定性等指标
    from data_source.data_fetcher import fetch_stock_data
    from datetime import timedelta
    
    scored_stocks = []
    for stock in stocks:
        # 获取近期数据来计算流动性等指标
        end_date = datetime.now().strftime('%Y%m%d')
        start_date = (datetime.now() - timedelta(days=30)).strftime('%Y%m%d')
        stock_data = fetch_stock_data(stock.symbol, start_date, end_date)
        
        if not stock_data.empty and len(stock_data) >= 10:
            # 计算平均日成交量
            avg_volume = stock_data['volume'].mean() if 'volume' in stock_data.columns else 0
            
            # 计算价格稳定性（标准差越小越稳定）
            prices = stock_data['close_price']
            price_volatility = prices.std() / prices.mean() if prices.mean() != 0 else float('inf')
            
            # 计算换手率（流动性指标）
            avg_turnover = avg_volume * prices.iloc[-1] if avg_volume and not prices.empty else 0
        else:
            avg_volume = 0
            price_volatility = float('inf')
            avg_turnover = 0
        
        # 计算机构持仓评分
        # 大市值 + 高流动性 + 价格稳定 = 高分
        market_cap_score = min((stock.market_cap or 0) / 10000000000, 10)  # 市值评分，最高10分
        liquidity_score = min(avg_volume / 50000000, 10) if avg_volume else 0  # 流动性评分
        stability_score = max(10 - price_volatility * 100, 0)  # 稳定性评分
        
        total_score = (market_cap_score * 0.5 + liquidity_score * 0.3 + stability_score * 0.2) * 10
        
        scored_stocks.append({
            'stock': stock.to_dict(),
            'score': total_score,
            'avg_volume': int(avg_volume) if avg_volume else 0,
            'price_volatility': round(price_volatility, 4) if price_volatility != float('inf') else None,
            'avg_turnover': avg_turnover
        })
    
    # 按评分排序
    scored_stocks.sort(key=lambda x: x['score'], reverse=True)
    
    # 返回评分最高的股票作为机构重仓股候选
    result = {
        'filters': filters,
        'timestamp': datetime.now().isoformat(),
        'institutional_heavy_holding': [item['stock'] for item in scored_stocks[:20]],  # 前20只
        'top_candidates': [
            {
                'stock': item['stock'],
                'score': round(item['score'], 2),
                'avg_volume': item['avg_volume'],
                'price_volatility': item['price_volatility'],
                'avg_turnover': round(item['avg_turnover'], 2) if item['avg_turnover'] else 0
            }
            for item in scored_stocks[:20]
        ]
    }
    
    # 保存分析结果到数据库
    save_analysis_result(None, 'institutional', json.dumps(result, ensure_ascii=False), 'internal_algorithm')
    
    return result

def analyze_small_cap_leaders(max_market_cap):
    """分析中小票龙头股"""
    from data_source.data_fetcher import fetch_stock_data
    from datetime import timedelta
    
    # 获取市值小于阈值的股票
    stocks = Stock.query.filter(Stock.market_cap <= max_market_cap).all()
    
    if not stocks:
        return {
            'max_market_cap': max_market_cap,
            'timestamp': datetime.now().isoformat(),
            'small_cap_leaders': [],
            'message': '未找到符合条件的小市值股票'
        }
    
    # 计算每只小票的综合评分（考虑成长性、动量、流动性等因素）
    scored_stocks = []
    for stock in stocks:
        # 获取近期数据来计算成长性指标
        end_date = datetime.now().strftime('%Y%m%d')
        start_date = (datetime.now() - timedelta(days=60)).strftime('%Y%m%d')  # 2个月数据
        stock_data = fetch_stock_data(stock.symbol, start_date, end_date)
        
        if not stock_data.empty and len(stock_data) >= 10:
            # 计算60日涨幅
            recent_price = stock_data.iloc[-1]['close_price']
            prev_price = stock_data.iloc[0]['close_price']
            if prev_price and prev_price != 0:
                price_change_pct = (recent_price - prev_price) / prev_price * 100
            else:
                price_change_pct = 0
            
            # 计算价格动量（近期涨幅）
            if len(stock_data) >= 20:
                mid_price = stock_data.iloc[-21]['close_price']  # 20日之前的收盘价
                if mid_price and mid_price != 0:
                    momentum = (recent_price - mid_price) / mid_price * 100
                else:
                    momentum = 0
            else:
                momentum = price_change_pct
            
            # 计算平均成交量
            avg_volume = stock_data['volume'].mean() if 'volume' in stock_data.columns else 0
            
            # 计算价格波动率（风险指标）
            price_volatility = stock_data['close_price'].std() / stock_data['close_price'].mean() if stock_data['close_price'].mean() != 0 else float('inf')
        else:
            price_change_pct = 0
            momentum = 0
            avg_volume = 0
            price_volatility = float('inf')
        
        # 计算小票龙头评分
        # 市值适中(不是最小的) + 高涨幅 + 高动量 + 适中波动率 = 高分
        size_score = max(min((stock.market_cap or 0) / 1000000000, 5), 0.5)  # 市值评分，1-5分
        growth_score = max(min(price_change_pct, 100), -50) / 10  # 成长性评分，-5到10分
        momentum_score = max(min(momentum, 50), -25) / 5  # 动量评分，-5到10分
        risk_score = max(10 - price_volatility * 100, 0) if price_volatility != float('inf') else 0  # 风险评分
        
        total_score = (size_score * 0.2 + growth_score * 0.3 + momentum_score * 0.3 + risk_score * 0.2) * 10
        
        scored_stocks.append({
            'stock': stock.to_dict(),
            'score': total_score,
            'price_change_pct': round(price_change_pct, 2),
            'momentum': round(momentum, 2),
            'avg_volume': int(avg_volume) if avg_volume else 0,
            'price_volatility': round(price_volatility, 4) if price_volatility != float('inf') else None
        })
    
    # 按评分排序，只取前20只
    scored_stocks.sort(key=lambda x: x['score'], reverse=True)
    
    result = {
        'max_market_cap': max_market_cap,
        'timestamp': datetime.now().isoformat(),
        'small_cap_leaders': [item['stock'] for item in scored_stocks[:20]],
        'top_leaders': [
            {
                'stock': item['stock'],
                'score': round(item['score'], 2),
                'price_change_pct': item['price_change_pct'],
                'momentum': item['momentum'],
                'avg_volume': item['avg_volume'],
                'price_volatility': item['price_volatility']
            }
            for item in scored_stocks[:20]
        ]
    }
    
    # 保存分析结果到数据库
    save_analysis_result(None, 'small_cap_leader', json.dumps(result, ensure_ascii=False), 'internal_algorithm')
    
    return result

def analyze_undervalued_stocks(criteria):
    """分析低估股票"""
    # 这里实现低估股票的分析逻辑
    # 使用PE、PB、PEG等估值指标
    
    # 获取筛选条件
    pe_threshold = criteria.get('pe_threshold', 15)
    pb_threshold = criteria.get('pb_threshold', 1.5)
    peg_threshold = criteria.get('peg_threshold', 1.0)  # PEG阈值
    debt_to_asset_threshold = criteria.get('debt_to_asset_threshold', 0.6)  # 资产负债率阈值
    roe_threshold = criteria.get('roe_threshold', 0.1)  # ROE阈值
    
    # 基本估值筛选
    stocks = Stock.query.filter(
        Stock.pe_ratio < pe_threshold,
        Stock.pb_ratio < pb_threshold,
        Stock.pe_ratio > 0,  # 排除负值
        Stock.pb_ratio > 0,   # 排除负值
        Stock.pe_ratio != None,
        Stock.pb_ratio != None
    ).all()
    
    if not stocks:
        return {
            'criteria': criteria,
            'timestamp': datetime.now().isoformat(),
            'undervalued_stocks': [],
            'message': '未找到符合条件的低估股票'
        }
    
    # 对筛选出的股票进行进一步分析
    from data_source.data_fetcher import fetch_financial_indicators
    
    valued_stocks = []
    for stock in stocks:
        # 获取更多财务指标来计算综合估值评分
        financial_data = fetch_financial_indicators(stock.symbol)
        
        # 计算估值评分（越低越被低估）
        pe_score = (stock.pe_ratio or float('inf')) / pe_threshold if pe_threshold > 0 else float('inf')
        pb_score = (stock.pb_ratio or float('inf')) / pb_threshold if pb_threshold > 0 else float('inf')
        
        # 综合评分，考虑财务健康度
        valuation_score = (pe_score + pb_score) / 2  # 基础估值评分
        
        # 如果财务数据可用，加入财务健康度评分
        if financial_data is not None:
            # 这里可以加入更多的财务指标分析
            pass
        
        valued_stocks.append({
            'stock': stock.to_dict(),
            'valuation_score': valuation_score,  # 评分越低越被低估
            'pe_ratio': stock.pe_ratio,
            'pb_ratio': stock.pb_ratio
        })
    
    # 按估值评分升序排序（评分越低越被低估）
    valued_stocks.sort(key=lambda x: x['valuation_score'])
    
    result = {
        'criteria': criteria,
        'timestamp': datetime.now().isoformat(),
        'undervalued_stocks': [item['stock'] for item in valued_stocks[:20]],
        'detailed_analysis': [
            {
                'stock': item['stock'],
                'valuation_score': round(item['valuation_score'], 2),
                'pe_ratio': item['pe_ratio'],
                'pb_ratio': item['pb_ratio']
            }
            for item in valued_stocks[:20]
        ]
    }
    
    # 保存分析结果到数据库
    save_analysis_result(None, 'undervalued', json.dumps(result, ensure_ascii=False), 'internal_algorithm')
    
    return result

def analyze_small_cap_hot_stocks(max_market_cap):
    """分析小票热门股"""
    from data_source.data_fetcher import fetch_stock_data
    from datetime import timedelta
    
    # 获取市值小于阈值的股票
    stocks = Stock.query.filter(Stock.market_cap <= max_market_cap).all()
    
    if not stocks:
        return {
            'max_market_cap': max_market_cap,
            'timestamp': datetime.now().isoformat(),
            'small_cap_hot_stocks': [],
            'message': '未找到符合条件的小市值股票'
        }
    
    # 计算每只小票的热度评分（考虑成交量、价格涨幅、市场关注度等因素）
    hot_stocks = []
    for stock in stocks:
        # 获取近期数据来计算热度指标
        end_date = datetime.now().strftime('%Y%m%d')
        start_date = (datetime.now() - timedelta(days=20)).strftime('%Y%m%d')  # 20日数据
        stock_data = fetch_stock_data(stock.symbol, start_date, end_date)
        
        if not stock_data.empty and len(stock_data) >= 5:
            # 计算20日涨幅
            recent_price = stock_data.iloc[-1]['close_price']
            prev_price = stock_data.iloc[0]['close_price']
            if prev_price and prev_price != 0:
                price_change_pct = (recent_price - prev_price) / prev_price * 100
            else:
                price_change_pct = 0
            
            # 计算平均成交量
            avg_volume = stock_data['volume'].mean() if 'volume' in stock_data.columns else 0
            
            # 计算成交量增长率（与历史平均水平比较）
            if len(stock_data) > 10:
                prev_avg_volume = stock_data.iloc[:-10]['volume'].mean()  # 前10日平均成交量
                if prev_avg_volume and prev_avg_volume > 0:
                    volume_growth = (avg_volume - prev_avg_volume) / prev_avg_volume * 100
                else:
                    volume_growth = 0
            else:
                volume_growth = 0
            
            # 计算价格波动率
            price_volatility = stock_data['close_price'].std() / stock_data['close_price'].mean() if stock_data['close_price'].mean() != 0 else float('inf')
        else:
            price_change_pct = 0
            avg_volume = 0
            volume_growth = 0
            price_volatility = float('inf')
        
        # 计算热门股评分
        # 高涨幅 + 高成交量增长 + 高活跃度 = 高分
        growth_score = max(min(price_change_pct, 50), -20) / 5  # 涨幅评分，-4到10分
        volume_score = min(avg_volume / 10000000, 10) if avg_volume else 0  # 成交量评分，0-10分
        volume_growth_score = max(min(volume_growth, 200), 0) / 20  # 成交量增长评分，0-10分
        
        total_score = (growth_score * 0.4 + volume_score * 0.3 + volume_growth_score * 0.3) * 10
        
        hot_stocks.append({
            'stock': stock.to_dict(),
            'hot_score': total_score,
            'price_change_pct': round(price_change_pct, 2),
            'avg_volume': int(avg_volume) if avg_volume else 0,
            'volume_growth_pct': round(volume_growth, 2),
            'price_volatility': round(price_volatility, 4) if price_volatility != float('inf') else None
        })
    
    # 按热度评分排序
    hot_stocks.sort(key=lambda x: x['hot_score'], reverse=True)
    
    result = {
        'max_market_cap': max_market_cap,
        'timestamp': datetime.now().isoformat(),
        'small_cap_hot_stocks': [item['stock'] for item in hot_stocks[:20]],
        'top_hot_stocks': [
            {
                'stock': item['stock'],
                'hot_score': round(item['hot_score'], 2),
                'price_change_pct': item['price_change_pct'],
                'avg_volume': item['avg_volume'],
                'volume_growth_pct': item['volume_growth_pct'],
                'price_volatility': item['price_volatility']
            }
            for item in hot_stocks[:20]
        ]
    }
    
    # 保存分析结果到数据库
    save_analysis_result(None, 'small_cap_hot', json.dumps(result, ensure_ascii=False), 'internal_algorithm')
    
    return result

def analyze_market_trends():
    """分析市场整体趋势"""
    from data_source.data_fetcher import get_market_data_summary, fetch_sector_stocks
    from datetime import timedelta
    
    # 获取市场数据摘要
    market_data = get_market_data_summary()
    
    # 获取行业数据
    sector_data = {}
    # 这里可以获取各个行业的表现数据
    sectors = ['科技', '金融', '消费', '医疗', '制造']  # 示例行业
    for sector in sectors:
        sector_stocks = fetch_sector_stocks(sector)
        if sector_stocks:
            # 计算行业平均表现
            total_change = 0
            count = 0
            for stock in sector_stocks:
                # 获取股票近期涨跌幅
                from data_source.data_fetcher import fetch_stock_data
                end_date = datetime.now().strftime('%Y%m%d')
                start_date = (datetime.now() - timedelta(days=5)).strftime('%Y%m%d')
                stock_data = fetch_stock_data(stock.symbol, start_date, end_date)
                
                if not stock_data.empty and len(stock_data) >= 2:
                    recent_price = stock_data.iloc[-1]['close_price']
                    prev_price = stock_data.iloc[0]['close_price']
                    if prev_price and prev_price != 0:
                        price_change_pct = (recent_price - prev_price) / prev_price * 100
                        total_change += price_change_pct
                        count += 1
            
            if count > 0:
                sector_data[sector] = round(total_change / count, 2)
    
    # 使用AI生成市场趋势分析报告
    try:
        ai_response = ai_manager.generate_market_report(
            market_data=market_data or {},
            sector_data=sector_data
        )
        
        result = {
            'timestamp': datetime.now().isoformat(),
            'market_trend': 'analyzed_by_ai',
            'market_data': market_data,
            'sector_performance': sector_data,
            'ai_analysis': ai_response
        }
        ai_model_used = 'ai_model'
    except Exception as e:
        print(f"AI市场分析失败，使用基础分析: {str(e)}")
        
        # 基础市场分析
        result = {
            'timestamp': datetime.now().isoformat(),
            'market_trend': 'analyzed_by_algorithm',
            'market_data': market_data,
            'sector_performance': sector_data,
            'basic_analysis': {
                'overall_market': '市场整体表现平稳',
                'leading_sectors': sorted(sector_data.items(), key=lambda x: x[1], reverse=True)[:3],
                'trailing_sectors': sorted(sector_data.items(), key=lambda x: x[1])[:3],
                'investment_climate': '观望为主，注意风险'
            }
        }
        ai_model_used = 'internal_algorithm'
    
    # 保存分析结果到数据库
    save_analysis_result(None, 'market_trend', json.dumps(result, ensure_ascii=False), ai_model_used)
    
    return result

def ai_stock_analysis(symbol, analysis_type):
    """使用AI进行个股分析"""
    # 获取股票基本信息
    stock = Stock.query.filter_by(symbol=symbol).first()
    if not stock:
        raise ValueError(f"未找到股票: {symbol}")
    
    # 获取更详细的股票信息
    stock_info = fetch_stock_info(symbol)
    financial_data = fetch_financial_indicators(symbol)
    historical_data = fetch_stock_data(symbol)
    
    # 使用AI管理器进行分析
    try:
        ai_response = ai_manager.analyze_stock(
            symbol=symbol,
            company_name=stock.name,
            financial_data=financial_data or {},
            market_data={
                'stock_info': stock_info,
                'historical_data': historical_data.to_dict('records') if not historical_data.empty else [],
                'basic_info': stock.to_dict()
            },
            analysis_type=analysis_type
        )
        
        result = {
            'symbol': symbol,
            'analysis_type': analysis_type,
            'ai_analysis': ai_response,
            'timestamp': datetime.now().isoformat(),
            'data_sources': {
                'financial_data': financial_data is not None,
                'market_data': stock_info is not None,
                'historical_data': not historical_data.empty if 'historical_data' in locals() else False
            }
        }
    except Exception as e:
        # 如果AI分析失败，使用原始方法作为备选
        print(f"AI分析失败，使用基础分析: {str(e)}")
        ai_response = basic_ai_analysis(symbol, stock, analysis_type)
        result = {
            'symbol': symbol,
            'analysis_type': analysis_type,
            'ai_analysis': ai_response,
            'timestamp': datetime.now().isoformat(),
            'fallback': True
        }
    
    # 保存AI分析结果到数据库
    save_analysis_result(symbol, f'ai_{analysis_type}', json.dumps(result, ensure_ascii=False), 'ai_model')
    
    return result

def basic_ai_analysis(symbol, stock, analysis_type):
    """基础AI分析（备选方案）"""
    # 构造AI分析的提示
    if analysis_type == 'comprehensive':
        prompt = f"""
        请对股票 {stock.name}({symbol}) 进行全面分析。
        基本信息: {stock.to_dict()}
        
        请从以下维度进行分析:
        1. 基本面分析
        2. 技术面分析  
        3. 估值分析
        4. 风险提示
        5. 投资建议
        
        请提供详细的分析报告，并以结构化格式返回。
        """
    elif analysis_type == 'technical':
        prompt = f"请对股票 {stock.name}({symbol}) 进行技术面分析。请分析其技术走势、支撑位和阻力位、买卖信号等。"
    else:  # fundamental
        prompt = f"请对股票 {stock.name}({symbol}) 进行基本面分析。分析其行业地位、财务状况、成长潜力、竞争优势等。"
    
    # 调用AI服务获取分析结果（使用带回退的版本）
    return get_ai_response_with_fallback(prompt, 'qwen')

def save_analysis_result(symbol, analysis_type, result, ai_model_used):
    """保存分析结果到数据库"""
    from models import db, AnalysisResult
    
    analysis_result = AnalysisResult(
        stock_symbol=symbol,
        analysis_type=analysis_type,
        result=result,
        ai_model_used=ai_model_used
    )
    
    try:
        db.session.add(analysis_result)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        print(f"保存分析结果失败: {str(e)}")