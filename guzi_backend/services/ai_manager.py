# guzi_backend/services/ai_manager.py

from flask import current_app
from .ai_service import AIServiceAdapter
from .gemini_adapter import GeminiAdapter

class AIManager:
    """AI服务管理器，负责初始化和提供AI服务适配器。"""
    def __init__(self, app=None):
        self.adapters = {}
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        """根据应用配置初始化AI服务适配器。"""
        with app.app_context():
            # 初始化Gemini适配器
            gemini_api_key = current_app.config.get('GEMINI_API_KEY')
            if gemini_api_key:
                self.adapters['gemini'] = GeminiAdapter(gemini_api_key)
                print("Gemini AI service initialized.")
            else:
                print("Gemini API key not found. Gemini service not initialized.")

            # 可以在这里初始化其他AI服务，例如通义千问、火山引擎等

    def get_adapter(self, service_name: str = 'gemini') -> AIServiceAdapter:
        """获取指定名称的AI服务适配器。"""
        adapter = self.adapters.get(service_name)
        if adapter is None:
            raise ValueError(f"AI service '{service_name}' not found or not initialized.")
        return adapter

# 全局AI管理器实例
ai_manager = AIManager()
