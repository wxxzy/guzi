"""
模拟AI服务，用于开发和测试
"""
import random
import time
from typing import Dict, Any, Optional
from config import Config

class MockAIService:
    """模拟AI服务，用于开发和测试"""
    
    @staticmethod
    def get_mock_response(prompt: str, model_type: str = 'mock') -> str:
        """
        根据提示类型返回模拟响应
        """
        # 模拟API延迟
        time.sleep(0.5)
        
        if "分析" in prompt or "股票" in prompt:
            return MockAIService._generate_stock_analysis(prompt)
        elif "比较" in prompt:
            return MockAIService._generate_stock_comparison(prompt)
        elif "市场" in prompt:
            return MockAIService._generate_market_analysis(prompt)
        elif "投资建议" in prompt:
            return MockAIService._generate_investment_advice(prompt)
        else:
            # 生成通用AI响应
            responses = [
                "这是一个模拟AI响应。在实际部署中，这里将返回由AI模型生成的分析结果。",
                "根据您提供的信息，我们的AI模型会进行深入分析并生成专业建议。",
                "基于先进的人工智能算法，系统已完成相关分析任务。",
                "正在处理您的请求，请稍后查看AI分析结果。"
            ]
            return random.choice(responses)
    
    @staticmethod
    def _generate_stock_analysis(prompt: str) -> str:
        """生成股票分析模拟响应"""
        return f"""
        【AI股票分析报告】

        根据您的请求，对相关股票进行分析：

        1. 基本面分析：
           - 公司财务状况良好，营收稳定增长
           - 盈利能力较强，ROE维持在行业平均水平之上
           - 资产负债结构合理，偿债能力较强

        2. 技术面分析：
           - 当前价格处于上升通道中
           - 成交量配合良好，资金关注度较高
           - 技术指标显示短期有上涨动能

        3. 估值分析：
           - 当前市盈率低于行业平均水平
           - 存在一定的估值修复空间
           - 长期价值被市场低估

        4. 风险提示：
           - 宏观经济波动风险
           - 行业政策变化风险
           - 市场流动性风险

        5. 投资建议：
           - 短期：谨慎观望
           - 中期：逢低布局
           - 长期：积极关注

        注意：以上为模拟分析结果，仅供参考，不构成投资建议。
        """
    
    @staticmethod
    def _generate_stock_comparison(prompt: str) -> str:
        """生成股票比较模拟响应"""
        return f"""
        【AI股票对比分析报告】

        对比分析结果：

        股票A：
        - 优势：盈利能力强，品牌影响力大
        - 劣势：估值偏高，增长空间有限
        - 适合：稳健型投资者

        股票B：
        - 优势：成长性好，估值合理
        - 劣势：业绩波动较大，风险相对较高
        - 适合：成长型投资者

        综合评价：
        - 风险偏好低的投资者可选择股票A
        - 风险偏好高的投资者可选择股票B
        - 建议组合配置以分散风险

        注意：以上为模拟分析结果，仅供参考。
        """
    
    @staticmethod
    def _generate_market_analysis(prompt: str) -> str:
        """生成市场分析模拟响应"""
        return f"""
        【AI市场分析报告】

        市场整体表现：
        - 上证指数：3025.12点，涨幅0.45%
        - 深证成指：12156.78点，涨幅0.78%
        - 创业板指：2456.34点，涨幅1.12%

        行业表现：
        - 科技板块：+2.34%，领涨市场
        - 消费板块：+0.89%，稳步上涨
        - 金融板块：-0.23%，小幅回调
        - 医疗板块：+1.56%，表现强势

        市场情绪：中性偏乐观
        资金流向：主力资金净流入36.8亿元
        两市成交额：8970亿元，成交量维持高位

        后市展望：
        - 短期市场有望继续震荡上行
        - 关注政策面的进一步催化
        - 谨慎对待高位个股的回调风险

        注意：以上为模拟分析结果，仅供参考。
        """
    
    @staticmethod
    def _generate_investment_advice(prompt: str) -> str:
        """生成投资建议模拟响应"""
        return f"""
        【AI个性化投资建议】

        基于您的风险偏好和市场情况，提供以下建议：

        1. 资产配置建议：
           - 股票类资产：60%
           - 固定收益类：30%
           - 现金类：10%

        2. 板块配置建议：
           - 科技板块：25%（重点关注人工智能、新能源）
           - 消费板块：20%（优选龙头企业）
           - 医疗板块：15%（长期价值投资）
           - 金融板块：10%（稳定收益）

        3. 操作建议：
           - 采取分批建仓策略
           - 设置合理的止损止盈点
           - 保持长期投资理念

        4. 风险管理：
           - 控制单一股票仓位不超20%
           - 定期调整投资组合
           - 关注宏观经济变化

        免责声明：投资有风险，入市需谨慎。以上建议仅供参考，不构成具体投资操作建议。
        """

# 如果配置中没有有效的API密钥，则使用模拟服务
def get_ai_response_with_fallback(prompt: str, model_type: str = 'qwen', **kwargs) -> str:
    """
    获取AI响应，如果真实API不可用则使用模拟服务
    """
    from ai_services.ai_client import get_ai_response, AIServiceError
    
    # 尝试使用真实的AI服务
    try:
        # 检查是否有配置API密钥
        if model_type == 'qwen' and Config.QWEN_API_KEY and Config.QWEN_API_KEY != 'your_qwen_api_key_here':
            return get_ai_response(prompt, model_type, **kwargs)
        elif model_type == 'volc' and Config.VOLC_API_KEY and Config.VOLC_API_KEY != '364f90b5-b03e-4cc6-b867-f9725ff85bfd':
            return get_ai_response(prompt, model_type, **kwargs)
        elif model_type == 'openai' and Config.OPENAI_API_KEY and Config.OPENAI_API_KEY != 'your_openai_api_key_here':
            return get_ai_response(prompt, model_type, **kwargs)
        else:
            # 如果配置的是默认示例密钥或者为空，使用模拟服务
            print(f"未配置有效的{model_type} API密钥，使用模拟服务...")
            return MockAIService.get_mock_response(prompt, model_type)
    except AIServiceError as e:
        print(f"真实AI服务调用失败: {str(e)}，使用模拟服务...")
        return MockAIService.get_mock_response(prompt, model_type)
    except Exception as e:
        print(f"AI服务调用异常: {str(e)}，使用模拟服务...")
        return MockAIService.get_mock_response(prompt, model_type)