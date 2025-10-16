# guzi_backend/services/gemini_adapter.py

import google.generativeai as genai
from .ai_service import BaseAIServiceAdapter
import json

class GeminiAdapter(BaseAIServiceAdapter):
    """Gemini AI服务适配器。"""

    def __init__(self, api_key: str):
        super().__init__(api_key)
        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel('gemini-2.5-flash') # 可以根据需要选择不同的模型

    def generate_text(self, prompt: str) -> str:
        """使用Gemini模型生成文本。"""
        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            self._handle_api_error(e)
            return ""

    def analyze_sentiment(self, text: str) -> dict:
        """使用Gemini模型分析文本情绪。
        
        这里通过prompt工程实现情绪分析，实际应用中可能需要更复杂的模型或API。
        """
        sentiment_prompt = f"""请分析以下文本的情绪，并以JSON格式返回结果。情绪分为'积极'、'消极'、'中性'。同时给出情绪得分（-1到1之间，-1为最消极，1为最积极）。

        文本: ""{text} ""

        JSON格式示例:
        {{"sentiment": "积极", "score": 0.8}}
        """
        try:
            response = self.model.generate_content(sentiment_prompt)
            # 尝试解析JSON，如果失败则返回默认值
            try:
                sentiment_result = json.loads(response.text)
                return sentiment_result
            except json.JSONDecodeError:
                print(f"Gemini sentiment analysis returned non-JSON: {response.text}")
                return {"sentiment": "中性", "score": 0.0}
        except Exception as e:
            self._handle_api_error(e)
            return {"sentiment": "中性", "score": 0.0}
