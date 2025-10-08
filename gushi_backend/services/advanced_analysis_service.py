"""
高级AI分析服务，处理复杂的金融分析任务
"""
from ai_services.ai_manager import ai_manager
from data_source.data_fetcher import fetch_stock_data, fetch_financial_indicators, get_market_data_summary
from services.scoring_service import calculate_comprehensive_score
from datetime import datetime, timedelta
import pandas as pd

class AdvancedAnalysisService:
    """高级分析服务类"""
    
    @staticmethod
    def analyze_multi_stock_correlation(symbols, days=60):
        """
        分析多只股票之间的相关性
        :param symbols: 股票代码列表
        :param days: 分析天数
        :return: 相关性分析结果
        """
        try:
            stock_data_dict = {}
            
            # 获取每只股票的历史数据
            for symbol in symbols:
                end_date = datetime.now().strftime('%Y%m%d')
                start_date = (datetime.now() - timedelta(days=days)).strftime('%Y%m%d')
                stock_data = fetch_stock_data(symbol, start_date, end_date)
                
                if not stock_data.empty:
                    # 计算每日收益率
                    stock_data['return'] = stock_data['close_price'].pct_change()
                    stock_data_dict[symbol] = stock_data['return'].dropna()
            
            if len(stock_data_dict) < 2:
                return {"error": "至少需要2只股票的数据才能进行相关性分析"}
            
            # 创建相关性矩阵
            combined_data = pd.DataFrame(stock_data_dict)
            correlation_matrix = combined_data.corr()
            
            # 提取主要相关性信息
            correlations = []
            for i, sym1 in enumerate(symbols):
                for j, sym2 in enumerate(symbols):
                    if i < j:  # 避免重复和自相关
                        corr_value = correlation_matrix.loc[sym1, sym2]
                        correlations.append({
                            "stock1": sym1,
                            "stock2": sym2,
                            "correlation": round(float(corr_value), 4) if not pd.isna(corr_value) else 0
                        })
            
            # 使用AI解释相关性结果
            correlation_desc = ai_manager.get_ai_response_with_fallback(
                f"请解释以下股票之间的相关性分析结果：{correlations}。"
                f"说明高相关性或低相关性的投资含义。", 
                'qwen'
            )
            
            return {
                "timestamp": datetime.now().isoformat(),
                "analysis_period": f"{days}天",
                "correlations": correlations,
                "ai_interpretation": correlation_desc,
                "type": "correlation_analysis"
            }
            
        except Exception as e:
            return {"error": f"相关性分析失败: {str(e)}"}
    
    @staticmethod
    def predict_stock_price(symbol, days=30):
        """
        基于AI的股价预测
        :param symbol: 股票代码
        :param days: 预测天数
        :return: 预测结果
        """
        try:
            # 获取历史数据
            end_date = datetime.now().strftime('%Y%m%d')
            start_date = (datetime.now() - timedelta(days=180)).strftime('%Y%m%d')  # 获取半年数据
            stock_data = fetch_stock_data(symbol, start_date, end_date)
            
            if stock_data.empty:
                return {"error": f"无法获取股票 {symbol} 的历史数据"}
            
            # 整合股票信息和历史数据
            from models import Stock
            stock_info = Stock.query.filter_by(symbol=symbol).first()
            
            # 使用AI进行预测分析
            prompt = f"""
            股票代码: {symbol}
            历史价格数据: {stock_data.tail(30).to_dict('records')}  # 最近30天数据
            基本信息: {stock_info.to_dict() if stock_info else {}}
            
            请基于以上信息预测未来{days}天的股价走势，包括:
            1. 价格趋势预测
            2. 关键支撑位和阻力位
            3. 风险因素
            4. 投资建议
            """
            
            prediction = ai_manager.get_ai_response_with_fallback(prompt, 'qwen', max_tokens=2000)
            
            return {
                "symbol": symbol,
                "prediction_days": days,
                "prediction": prediction,
                "timestamp": datetime.now().isoformat(),
                "type": "price_prediction"
            }
            
        except Exception as e:
            return {"error": f"股价预测失败: {str(e)}"}
    
    @staticmethod
    def analyze_market_regime(market_data=None):
        """
        分析市场状态（牛市、熊市、震荡市）
        :param market_data: 市场数据
        :return: 市场状态分析
        """
        try:
            if market_data is None:
                market_data = get_market_data_summary()
            
            # 使用AI分析市场状态
            prompt = f"""
            基于以下市场数据，分析当前市场状态：
            
            {market_data}
            
            请判断当前市场处于：
            1. 牛市
            2. 熊市 
            3. 震荡市
            
            并说明判断依据和投资策略建议。
            """
            
            regime_analysis = ai_manager.get_ai_response_with_fallback(prompt, 'qwen', max_tokens=1500)
            
            return {
                "market_data": market_data,
                "regime_analysis": regime_analysis,
                "timestamp": datetime.now().isoformat(),
                "type": "market_regime_analysis"
            }
            
        except Exception as e:
            return {"error": f"市场状态分析失败: {str(e)}"}
    
    @staticmethod
    def generate_risk_assessment(stock_symbols, portfolio_value=None):
        """
        生成风险评估报告
        :param stock_symbols: 股票代码列表
        :param portfolio_value: 投资组合总值
        :return: 风险评估结果
        """
        try:
            stocks_data = []
            
            # 获取每只股票的信息
            for symbol in stock_symbols:
                from models import Stock
                stock_info = Stock.query.filter_by(symbol=symbol).first()
                
                if stock_info:
                    scores = calculate_comprehensive_score(symbol)
                    stocks_data.append({
                        "symbol": symbol,
                        "info": stock_info.to_dict(),
                        "scores": scores
                    })
            
            # 使用AI生成风险评估
            prompt = f"""
            投资组合包含以下股票：
            {stocks_data}
            
            投资组合总值: {portfolio_value}
            
            请进行详细的风险评估，包括:
            1. 个股风险分析
            2. 组合风险分析
            3. 系统性风险
            4. 风险等级评定
            5. 风险管控建议
            """
            
            risk_assessment = ai_manager.get_ai_response_with_fallback(prompt, 'qwen', max_tokens=2000)
            
            return {
                "portfolio": {
                    "symbols": stock_symbols,
                    "stocks_data": stocks_data,
                    "total_value": portfolio_value
                },
                "risk_assessment": risk_assessment,
                "timestamp": datetime.now().isoformat(),
                "type": "risk_assessment"
            }
            
        except Exception as e:
            return {"error": f"风险评估失败: {str(e)}"}

# 创建高级分析服务实例
advanced_analysis_service = AdvancedAnalysisService()