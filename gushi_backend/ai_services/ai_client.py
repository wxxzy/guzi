import openai
import requests
import json
import time
import logging
from config import Config
from typing import Optional, Dict, Any

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AIServiceError(Exception):
    """AI服务相关的自定义异常"""
    pass

def get_ai_response(
    prompt: str, 
    model_type: str = 'volc', 
    model_name: Optional[str] = None,
    temperature: float = 0.7,
    max_tokens: int = 2000
) -> str:
    """
    获取AI模型的响应
    :param prompt: 提示文本
    :param model_type: 模型类型 ('qwen', 'volc', 'openai')
    :param model_name: 具体模型名称（可选，如果不提供则使用配置中的默认模型）
    :param temperature: 温度参数
    :param max_tokens: 最大token数
    :return: AI模型的响应
    """
    try:
        if model_type == 'qwen':
            return call_qwen_api(prompt, model_name, temperature, max_tokens)
        elif model_type == 'volc':
            return call_volc_api(prompt, model_name, temperature, max_tokens)
        elif model_type == 'openai':
            return call_openai_api(prompt, model_name, temperature, max_tokens)
        else:
            # 默认使用Qwen
            return call_qwen_api(prompt, model_name, temperature, max_tokens)
    except Exception as e:
        logger.error(f"调用AI服务 {model_type} 失败: {str(e)}")
        raise AIServiceError(f"AI服务调用失败: {str(e)}")

def call_qwen_api(
    prompt: str, 
    model_name: Optional[str] = None, 
    temperature: float = 0.7, 
    max_tokens: int = 2000
) -> str:
    """调用通义千问API"""
    try:
        if not Config.QWEN_API_KEY:
            raise AIServiceError("未配置通义千问API密钥")
        
        # 使用dashscope兼容的OpenAI客户端
        client = openai.OpenAI(
            api_key=Config.QWEN_API_KEY,
            base_url=Config.QWEN_BASE_URL
        )
        
        # 如果没有指定模型名称，使用默认模型
        model = model_name or "qwen-max"
        
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "user", "content": prompt}
            ],
            temperature=temperature,
            max_tokens=max_tokens
        )
        
        content = response.choices[0].message.content
        logger.info(f"通义千问API调用成功，返回长度: {len(content) if content else 0}")
        return content
        
    except Exception as e:
        error_msg = f"调用通义千问API失败: {str(e)}"
        logger.error(error_msg)
        raise AIServiceError(error_msg)

def call_volc_api(
    prompt: str, 
    model_name: Optional[str] = None, 
    temperature: float = 0.7, 
    max_tokens: int = 2000
) -> str:
    """调用火山引擎API（使用OpenAI SDK方式）"""
    try:
        if not Config.VOLC_API_KEY:
            raise AIServiceError("未配置火山引擎API密钥")
        
        # 使用OpenAI SDK方式调用火山引擎API
        client = openai.OpenAI(
            api_key=Config.VOLC_API_KEY,
            base_url=Config.VOLC_BASE_URL
        )
        
        # 使用配置中的模型名称或传入的模型名称
        model = model_name or Config.VOLC_MODEL_NAME
        if not model:
            raise AIServiceError("未配置火山引擎模型名称")
        
        logger.info(f"调用火山引擎API，模型: {model}")
        
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "user", "content": prompt}
            ],
            temperature=temperature,
            max_tokens=max_tokens
        )
        
        content = response.choices[0].message.content
        logger.info(f"火山引擎API调用成功，返回长度: {len(content) if content else 0}")
        return content
        
    except Exception as e:
        error_msg = f"调用火山引擎API失败: {str(e)}"
        logger.error(error_msg)
        raise AIServiceError(error_msg)

def call_openai_api(
    prompt: str, 
    model_name: Optional[str] = None, 
    temperature: float = 0.7, 
    max_tokens: int = 2000
) -> str:
    """调用OpenAI API"""
    try:
        if not Config.OPENAI_API_KEY:
            raise AIServiceError("未配置OpenAI API密钥")
        
        # 配置OpenAI客户端
        client = openai.OpenAI(api_key=Config.OPENAI_API_KEY)
        
        # 如果没有指定模型名称，使用默认模型
        model = model_name or "gpt-3.5-turbo"
        
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "user", "content": prompt}
            ],
            temperature=temperature,
            max_tokens=max_tokens
        )
        
        content = response.choices[0].message.content
        logger.info(f"OpenAI API调用成功，返回长度: {len(content) if content else 0}")
        return content
        
    except Exception as e:
        error_msg = f"调用OpenAI API失败: {str(e)}"
        logger.error(error_msg)
        raise AIServiceError(error_msg)

def select_best_ai_service(
    prompt: str, 
    services: list = None,
    model_names: Dict[str, str] = None,
    temperature: float = 0.7,
    max_tokens: int = 2000,
    retry_count: int = 2
) -> str:
    """
    选择最佳AI服务
    :param prompt: 提示文本
    :param services: 可用服务列表
    :param model_names: 各服务对应的模型名称字典
    :param temperature: 温度参数
    :param max_tokens: 最大token数
    :param retry_count: 重试次数
    :return: 最佳响应
    """
    if services is None:
        services = ['qwen', 'volc', 'openai']
    
    if model_names is None:
        model_names = {}
    
    for service in services:
        for attempt in range(retry_count + 1):
            try:
                model_name = model_names.get(service)
                response = get_ai_response(prompt, service, model_name, temperature, max_tokens)
                
                if response and len(response.strip()) > 10:  # 确保响应有效
                    logger.info(f"使用 {service} 服务成功获得有效响应")
                    return response
                else:
                    logger.warning(f"{service} 服务返回的响应无效或过短")
            except AIServiceError as e:
                logger.warning(f"尝试使用 {service} 服务第 {attempt + 1} 次失败: {str(e)}")
                if attempt < retry_count:
                    time.sleep(1 * (attempt + 1))  # 递增延迟
                continue
            except Exception as e:
                logger.error(f"意外错误使用 {service} 服务: {str(e)}")
                continue
    
    raise AIServiceError("所有AI服务均不可用")

def test_ai_connection(model_type: str) -> Dict[str, Any]:
    """
    测试AI服务连接
    :param model_type: 模型类型
    :return: 测试结果
    """
    try:
        test_prompt = "你好，请简单介绍一下你自己。"
        response = get_ai_response(test_prompt, model_type, max_tokens=100)
        
        return {
            "success": True,
            "response_length": len(response) if response else 0,
            "sample_response": response[:100] + "..." if response and len(response) > 100 else response
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }

def get_available_services() -> Dict[str, bool]:
    """
    获取可用的AI服务列表
    :return: 服务可用性字典
    """
    services = {
        'qwen': False,
        'volc': False,
        'openai': False
    }
    
    # 测试每个服务是否配置了API密钥
    if Config.QWEN_API_KEY:
        result = test_ai_connection('qwen')
        services['qwen'] = result['success']
    
    if Config.VOLC_API_KEY:
        result = test_ai_connection('volc')
        services['volc'] = result['success']
    
    if Config.OPENAI_API_KEY:
        result = test_ai_connection('openai')
        services['openai'] = result['success']
    
    return services