# guzi_backend/services/ai_service.py

from abc import ABC, abstractmethod

class AIServiceAdapter(ABC):
    """AI服务适配器抽象基类。"""

    @abstractmethod
    def generate_text(self, prompt: str) -> str:
        """根据给定的提示生成文本。"""
        pass

    @abstractmethod
    def analyze_sentiment(self, text: str) -> dict:
        """分析给定文本的情绪。"""
        pass

    # 可以根据需要添加更多抽象方法，例如：
    # @abstractmethod
    # def summarize_text(self, text: str) -> str:
    #     """总结给定文本。"""
    #     pass

class BaseAIServiceAdapter(AIServiceAdapter):
    """基础AI服务适配器，提供通用功能。"""
    def __init__(self, api_key: str):
        self.api_key = api_key

    def _handle_api_error(self, e: Exception):
        """处理API调用中可能出现的错误。"""
        print(f"AI Service API Error: {e}")
        # 这里可以添加更复杂的错误处理逻辑，例如日志记录、告警等
        raise e

    # 抽象方法在子类中实现
