"""
AI服务管理器，提供高级AI功能
"""
import logging
from typing import Dict, List, Optional
from dataclasses import dataclass
from config import Config
from ai_services.ai_client import select_best_ai_service, get_available_services
from ai_services.mock_ai_service import get_ai_response_with_fallback
import json
import re
from datetime import datetime

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class AIModelConfig:
    """AI模型配置"""
    model_type: str  # 'qwen', 'volc', 'openai'
    model_name: Optional[str] = None
    temperature: float = 0.7
    max_tokens: int = 2000
    priority: int = 1  # 优先级，数字越小优先级越高

class AIServiceManager:
    """AI服务管理器"""
    
    def __init__(self):
        self.default_models = {
            'qwen': AIModelConfig('qwen', 'qwen-max', 0.7, 2000, 1),
            'volc': AIModelConfig('volc', Config.VOLC_MODEL_NAME, 0.7, 2000, 2),
            'openai': AIModelConfig('openai', 'gpt-3.5-turbo', 0.7, 2000, 3)
        }
        self.available_services = get_available_services()
    
    def analyze_stock(self, symbol: str, company_name: str, financial_data: Dict, market_data: Dict, analysis_type: str = "comprehensive") -> str:
        """
        分析股票
        :param symbol: 股票代码
        :param company_name: 公司名称
        :param financial_data: 财务数据
        :param market_data: 市场数据
        :param analysis_type: 分析类型
        :return: 分析结果
        """
        # 根据分析类型构建不同的提示
        if analysis_type == "comprehensive":
            prompt = self._build_comprehensive_analysis_prompt(symbol, company_name, financial_data, market_data)
        elif analysis_type == "technical":
            prompt = self._build_technical_analysis_prompt(symbol, company_name, market_data)
        elif analysis_type == "fundamental":
            prompt = self._build_fundamental_analysis_prompt(symbol, company_name, financial_data)
        elif analysis_type == "valuation":
            prompt = self._build_valuation_analysis_prompt(symbol, company_name, financial_data, market_data)
        else:
            prompt = self._build_comprehensive_analysis_prompt(symbol, company_name, financial_data, market_data)
        
        # 选择最佳AI服务进行分析
        try:
            return select_best_ai_service(
                prompt=prompt,
                services=self._get_priority_services(),
                temperature=0.6,  # 对于分析任务，稍微降低随机性
                max_tokens=3000
            )
        except Exception as e:
            logger.warning(f"选择AI服务失败: {str(e)}，使用默认服务...")
            # 如果选择最佳服务失败，使用回退机制
            return get_ai_response_with_fallback(prompt, 'volc', temperature=0.6, max_tokens=3000)
    
    def generate_investment_advice(self, user_profile: Dict, market_conditions: Dict, stock_analysis: str) -> str:
        """
        生成投资建议
        :param user_profile: 用户画像（风险偏好、投资目标等）
        :param market_conditions: 市场情况
        :param stock_analysis: 股票分析结果
        :return: 投资建议
        """
        prompt = f"""
        基于以下信息为投资者生成个性化的投资建议：

        投资者画像：
        {user_profile}

        当前市场情况：
        {market_conditions}

        股票分析结果：
        {stock_analysis}

        请提供具体的投资建议，包括：
        1. 是否建议买入、持有或卖出
        2. 建议的投资比例
        3. 风险提示
        4. 未来展望
        5. 操作策略

        请注意：投资有风险，建议仅供参考，不构成投资建议。
        """
        
        # 选择最佳AI服务进行分析
        try:
            return select_best_ai_service(
                prompt=prompt,
                services=self._get_priority_services(),
                temperature=0.5,  # 对于投资建议，进一步降低随机性
                max_tokens=2000
            )
        except Exception as e:
            logger.warning(f"选择AI服务失败: {str(e)}，使用默认服务...")
            return get_ai_response_with_fallback(prompt, model_type='volc', temperature=0.5, max_tokens=2000)
    
    def compare_stocks(self, stock1_info: Dict, stock2_info: Dict) -> str:
        """
        比较两只股票
        :param stock1_info: 第一只股票信息
        :param stock2_info: 第二只股票信息
        :return: 比较分析结果
        """
        prompt = f"""
        请对以下两只股票进行比较分析：

        股票1：{stock1_info}
        股票2：{stock2_info}

        请从以下维度进行比较：
        1. 基本面分析
        2. 估值水平
        3. 成长性
        4. 风险因素
        5. 投资价值

        最后给出综合评价和投资建议。
        """
        
        try:
            return select_best_ai_service(
                prompt=prompt,
                services=self._get_priority_services(),
                temperature=0.6,
                max_tokens=2500
            )
        except Exception as e:
            logger.warning(f"选择AI服务失败: {str(e)}，使用默认服务...")
            return get_ai_response_with_fallback(prompt, model_type='volc', temperature=0.6, max_tokens=2500)
    
    def generate_market_report(self, market_data: Dict, sector_data: Dict) -> str:
        """
        生成市场报告
        :param market_data: 市场整体数据
        :param sector_data: 行业数据
        :return: 市场报告
        """
        prompt = f"""
        基于以下市场数据生成一份专业的市场分析报告：

        市场整体数据：
        {market_data}

        行业数据：
        {sector_data}

        报告应包括：
        1. 市场整体表现概述
        2. 主要行业表现分析
        3. 市场趋势判断
        4. 投资机会识别
        5. 风险提示
        6. 未来展望

        请用专业但易懂的语言描述。
        """
        
        try:
            return select_best_ai_service(
                prompt=prompt,
                services=self._get_priority_services(),
                temperature=0.7,
                max_tokens=3000
            )
        except Exception as e:
            logger.warning(f"选择AI服务失败: {str(e)}，使用默认服务...")
            return get_ai_response_with_fallback(prompt, model_type='volc', temperature=0.7, max_tokens=3000)
    
    def get_recommendation_for_profile(self, user_profile: Dict, market_context: str) -> List[Dict]:
        """
        根据用户画像推荐股票
        :param user_profile: 用户画像
        :param market_context: 市场上下文
        :return: 推荐股票列表
        """
        prompt = f"""
        基于以下用户画像和市场情况，推荐适合的股票投资标的：

        用户画像：
        {user_profile}

        市场情况：
        {market_context}

        请推荐3-5只股票，并为每只股票提供：
        1. 股票代码和名称
        2. 推荐理由
        3. 适合的投资周期
        4. 预期收益和风险
        5. 建议仓位比例

        推荐应多样化，包含不同行业和市值的股票。
        """
        
        try:
            response = select_best_ai_service(
                prompt=prompt,
                services=self._get_priority_services(),
                temperature=0.6,
                max_tokens=2500
            )
        except Exception as e:
            logger.warning(f"选择AI服务失败: {str(e)}，使用默认服务...")
            response = get_ai_response_with_fallback(prompt, model_type='volc', temperature=0.6, max_tokens=2500)
        
        # 解析响应并返回结构化数据
        # 这里简化处理，实际应用中可能需要更复杂的解析逻辑
        return [{"raw_response": response}]
    
    def _build_comprehensive_analysis_prompt(self, symbol: str, company_name: str, financial_data: Dict, market_data: Dict) -> str:
        """构建综合分析提示"""
        return f"""
        请对{company_name}({symbol})进行综合分析，包含以下方面：

        财务数据：
        {financial_data}

        市场数据：
        {market_data}

        请从以下维度进行深入分析：
        1. 基本面分析（财务状况、盈利能力、成长性等）
        2. 技术面分析（股价走势、技术指标、支撑阻力位等）
        3. 估值分析（市盈率、市净率、PEG等指标）
        4. 行业地位和竞争优势
        5. 未来发展前景
        6. 潜在风险
        7. 投资建议

        请提供详细、专业且客观的分析。
        """
    
    def _build_technical_analysis_prompt(self, symbol: str, company_name: str, market_data: Dict) -> str:
        """构建技术分析提示"""
        return f"""
        请对{company_name}({symbol})进行技术面分析，基于以下市场数据：

        {market_data}

        请分析：
        1. 价格走势和技术形态
        2. 主要技术指标（MACD、RSI、KDJ等）
        3. 支撑位和阻力位
        4. 交易量分析
        5. 短中长期技术前景
        6. 买卖信号判断

        请提供具体的技术分析结论。
        """
    
    def _build_fundamental_analysis_prompt(self, symbol: str, company_name: str, financial_data: Dict) -> str:
        """构建基本面分析提示"""
        return f"""
        请对{company_name}({symbol})进行基本面分析，基于以下财务数据：

        {financial_data}

        请分析：
        1. 盈利能力（ROE、ROA、净利润率等）
        2. 偿债能力（资产负债率、流动比率等）
        3. 营运能力（存货周转率、应收帐款周转率等）
        4. 成长性（收入增长率、净利润增长率等）
        5. 现金流状况
        6. 业务模式和竞争优势
        7. 行业地位

        请提供详细的基本面评估。
        """
    
    def _build_valuation_analysis_prompt(self, symbol: str, company_name: str, financial_data: Dict, market_data: Dict) -> str:
        """构建估值分析提示"""
        return f"""
        请对{company_name}({symbol})进行估值分析，基于以下数据：

        财务数据：
        {financial_data}

        市场数据：
        {market_data}

        请使用多种估值方法进行分析：
        1. 市盈率估值（历史PE、行业PE对比）
        2. 市净率估值
        3. 现金流折现估值（如可能）
        4. EV/EBITDA估值
        5. PEG估值

        综合判断当前股价是否被高估或低估，并给出目标价格区间。
        """
    
    def _get_priority_services(self) -> List[str]:
        """获取按优先级排序的服务列表"""
        # 根据配置的优先级排序
        sorted_models = sorted(self.default_models.values(), key=lambda x: x.priority)
        return [model.model_type for model in sorted_models if self.available_services.get(model.model_type, False)]
    
    def get_service_status(self) -> Dict:
        """获取服务状态"""
        return {
            "available_services": self.available_services,
            "default_models": {k: v.model_name for k, v in self.default_models.items()},
            "priority_order": self._get_priority_services()
        }

    def process_natural_language_query(self, query: str, user_context: Dict = None) -> Dict:
        """
        处理自然语言查询
        :param query: 用户查询
        :param user_context: 用户上下文
        :return: 查询结果
        """
        try:
            # 解析用户查询意图
            intent = self._parse_query_intent(query)
            
            # 根据意图执行相应操作
            if intent['type'] == 'stock_info':
                return self._handle_stock_info_query(intent, user_context)
            elif intent['type'] == 'analysis_request':
                return self._handle_analysis_query(intent, user_context)
            elif intent['type'] == 'comparison':
                return self._handle_comparison_query(intent, user_context)
            elif intent['type'] == 'market_overview':
                return self._handle_market_query(intent, user_context)
            else:
                # 使用AI直接回答
                return self._handle_general_query(query, user_context)
                
        except Exception as e:
            logger.error(f"自然语言查询处理失败: {str(e)}")
            return {"error": f"查询处理失败: {str(e)}", "type": "error"}

    def _parse_query_intent(self, query: str) -> Dict:
        """解析查询意图"""
        query_lower = query.lower()
        
        # 股票信息查询
        stock_pattern = r'(\w+股票|.*?的股票|股票\s*\w+)'
        stock_match = re.search(stock_pattern, query)
        
        # 分析类查询
        analysis_keywords = ['分析', '分析一下', '评价', '看法', '前景', '趋势', '走势']
        analysis_match = any(keyword in query for keyword in analysis_keywords)
        
        # 比较类查询
        comparison_keywords = ['比', '对比', '哪个好', '哪个强', '比较', 'vs', '和.*?哪个']
        comparison_match = any(keyword in query for keyword in comparison_keywords)
        
        # 市场类查询
        market_keywords = ['市场', '大盘', '行情', '走势', '趋势', '板块']
        market_match = any(keyword in query for keyword in market_keywords)
        
        # 提取股票代码或名称（简化版）
        symbol_pattern = r'([A-Z0-9]{5,6}|[a-z0-9]{5,6})'
        symbol_matches = re.findall(symbol_pattern, query)
        
        return {
            'type': 'stock_info' if (stock_match or symbol_matches) and not comparison_match else
                     'comparison' if comparison_match else
                     'market_overview' if market_match and not stock_match else
                     'analysis_request' if analysis_match else
                     'general',
            'query': query,
            'symbols': symbol_matches,
            'original_query': query
        }

    def _handle_stock_info_query(self, intent: Dict, user_context: Dict) -> Dict:
        """处理股票信息查询"""
        # 这里需要调用数据服务获取股票信息
        # 由于股票数据服务在其他模块，这里返回提示
        if intent['symbols']:
            result = {
                "type": "stock_info",
                "symbols": intent['symbols'],
                "message": f"正在查询股票 {', '.join(intent['symbols'])} 的信息...",
                "query": intent['original_query']
            }
        else:
            result = {
                "type": "stock_info",
                "message": "请提供具体的股票代码或名称",
                "query": intent['original_query']
            }
        
        return result

    def _handle_analysis_query(self, intent: Dict, user_context: Dict) -> Dict:
        """处理分析类查询"""
        # 构造分析提示
        prompt = f"""
        用户查询: {intent['original_query']}
        
        请提供专业的股票分析，包括:
        1. 相关股票的基本面分析
        2. 技术面分析
        3. 市场环境分析
        4. 风险提示
        5. 投资建议
        
        分析应当专业、客观、详尽。
        """
        
        try:
            response = get_ai_response_with_fallback(prompt, 'volc', max_tokens=2000)
            return {
                "type": "analysis_result",
                "query": intent['original_query'],
                "analysis": response
            }
        except Exception as e:
            return {
                "type": "error",
                "query": intent['original_query'],
                "error": str(e)
            }

    def _handle_comparison_query(self, intent: Dict, user_context: Dict) -> Dict:
        """处理比较类查询"""
        prompt = f"""
        用户查询: {intent['original_query']}
        
        请对相关股票进行对比分析，包括:
        1. 基本面对比
        2. 估值水平对比
        3. 成长性对比
        4. 风险因素对比
        5. 投资价值对比
        
        请给出明确的对比结果和建议。
        """
        
        try:
            response = get_ai_response_with_fallback(prompt, 'volc', max_tokens=2500)
            return {
                "type": "comparison_result", 
                "query": intent['original_query'],
                "comparison": response
            }
        except Exception as e:
            return {
                "type": "error",
                "query": intent['original_query'],
                "error": str(e)
            }

    def _handle_market_query(self, intent: Dict, user_context: Dict) -> Dict:
        """处理市场概览查询"""
        from data_source.data_fetcher import get_market_data_summary
        market_data = get_market_data_summary()
        
        prompt = f"""
        用户查询: {intent['original_query']}
        
        市场数据: {market_data}
        
        请分析当前市场情况，包括:
        1. 整体市场表现
        2. 主要板块表现
        3. 市场趋势判断
        4. 投资机会分析
        5. 风险提示
        """
        
        try:
            response = get_ai_response_with_fallback(prompt, 'volc', max_tokens=2000)
            return {
                "type": "market_analysis",
                "query": intent['original_query'],
                "market_data": market_data,
                "analysis": response
            }
        except Exception as e:
            return {
                "type": "error",
                "query": intent['original_query'],
                "error": str(e)
            }

    def _handle_general_query(self, query: str, user_context: Dict) -> Dict:
        """处理一般查询"""
        prompt = f"""
        用户查询: {query}
        
        用户上下文: {user_context}
        
        请提供专业的金融投资相关回答。
        """
        
        try:
            response = get_ai_response_with_fallback(prompt, 'volc', max_tokens=1500)
            return {
                "type": "general_response",
                "query": query,
                "response": response
            }
        except Exception as e:
            return {
                "type": "error",
                "query": query,
                "error": str(e)
            }

    def generate_personalized_recommendation(self, user_profile: Dict) -> Dict:
        """
        生成个性化推荐
        :param user_profile: 用户画像
        :return: 推荐结果
        """
        try:
            prompt = f"""
            用户画像:
            - 风险偏好: {user_profile.get('risk_tolerance', '中等')}
            - 投资目标: {user_profile.get('investment_goal', '稳健增值')}
            - 投资期限: {user_profile.get('investment_horizon', '中期')}
            - 资金规模: {user_profile.get('capital_size', '中等')}
            - 投资经验: {user_profile.get('investment_experience', '中等')}
            
            基于以上用户画像，请提供个性化的股票投资建议，包括:
            1. 适合的投资策略
            2. 推荐的股票池（3-5只）
            3. 资产配置建议
            4. 风险控制措施
            5. 操作建议
            """
            
            response = get_ai_response_with_fallback(prompt, 'volc', max_tokens=2500)
            
            return {
                "timestamp": datetime.now().isoformat(),
                "user_profile": user_profile,
                "recommendation": response,
                "type": "personalized_recommendation"
            }
        except Exception as e:
            logger.error(f"生成个性化推荐失败: {str(e)}")
            return {
                "error": str(e),
                "type": "error"
            }

    def sentiment_analysis(self, text: str) -> Dict:
        """
        情绪分析
        :param text: 待分析文本
        :return: 情绪分析结果
        """
        try:
            prompt = f"""
            请分析以下文本的情绪倾向:

            文本: {text}

            请从以下维度进行分析:
            1. 整体情绪（积极/消极/中性）
            2. 情绪强度（1-10分）
            3. 情绪标签（如: 乐观、悲观、焦虑、期待等）
            4. 关键情绪词汇
            """
            
            response = get_ai_response_with_fallback(prompt, 'volc', max_tokens=1000)
            
            return {
                "original_text": text,
                "sentiment_analysis": response,
                "type": "sentiment_analysis"
            }
        except Exception as e:
            logger.error(f"情绪分析失败: {str(e)}")
            return {
                "error": str(e),
                "type": "error"
            }

# 创建全局AI服务管理器实例
ai_manager = AIServiceManager()