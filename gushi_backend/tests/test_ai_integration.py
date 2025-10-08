"""
AI服务集成测试脚本
测试所有AI服务的集成情况
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ai_services.ai_client import get_ai_response, test_ai_connection, get_available_services
from config import Config

def test_all_ai_services():
    """测试所有AI服务"""
    print("=== AI服务集成测试 ===")
    
    # 显示配置信息
    print("\n--- 配置信息 ---")
    print(f"Qwen API Key: {'✓ 已配置' if Config.QWEN_API_KEY else '✗ 未配置'}")
    print(f"Volc API Key: {'✓ 已配置' if Config.VOLC_API_KEY else '✗ 未配置'}")
    print(f"OpenAI API Key: {'✓ 已配置' if Config.OPENAI_API_KEY else '✗ 未配置'}")
    
    # 获取可用服务
    print("\n--- 可用服务检查 ---")
    try:
        available_services = get_available_services()
        for service, available in available_services.items():
            status = "✓ 可用" if available else "✗ 不可用"
            print(f"{service}: {status}")
    except Exception as e:
        print(f"检查可用服务失败: {str(e)}")
        return
    
    # 测试每个服务
    services_to_test = ['qwen', 'volc', 'openai']
    
    for service in services_to_test:
        print(f"\n--- 测试 {service} 服务 ---")
        if not available_services.get(service, False):
            print(f"  {service} 服务不可用，跳过测试")
            continue
            
        # 测试连接
        print(f"  测试 {service} 连接...")
        try:
            result = test_ai_connection(service)
            if result['success']:
                print(f"  ✓ {service} 连接测试成功")
                print(f"    响应长度: {result['response_length']}")
            else:
                print(f"  ✗ {service} 连接测试失败: {result['error']}")
                continue
        except Exception as e:
            print(f"  ✗ {service} 连接测试异常: {str(e)}")
            continue
            
        # 测试具体调用
        print(f"  测试 {service} 具体调用...")
        try:
            response = get_ai_response(
                "请用一句话介绍人工智能。",
                service,
                max_tokens=50
            )
            print(f"  ✓ {service} 调用成功")
            print(f"    响应: {response[:100]}{'...' if len(response) > 100 else ''}")
        except Exception as e:
            print(f"  ✗ {service} 调用失败: {str(e)}")

def test_model_selection():
    """测试模型选择功能"""
    print("\n=== 模型选择测试 ===")
    
    # 测试火山引擎不同模型
    models_to_test = [
        Config.VOLC_MODEL_NAME,
        "doubao-pro-32k",
        "doubao-lite-128k"
    ]
    
    for model_name in models_to_test:
        if not model_name:
            continue
            
        print(f"\n  测试模型: {model_name}")
        try:
            response = get_ai_response(
                "你好，介绍一下你自己。",
                'volc',
                model_name=model_name,
                max_tokens=50
            )
            print(f"  ✓ 模型 {model_name} 调用成功")
            print(f"    响应: {response[:50]}...")
        except Exception as e:
            print(f"  ✗ 模型 {model_name} 调用失败: {str(e)}")

def main():
    """主测试函数"""
    print("开始AI服务集成测试...")
    
    try:
        test_all_ai_services()
        test_model_selection()
        
        print("\n=== AI服务集成测试完成 ===")
        print("🎉 所有测试完成！AI服务已成功集成。")
        
    except Exception as e:
        print(f"\n❌ 测试过程中出现错误: {str(e)}")
        print("请检查配置和网络连接。")

if __name__ == "__main__":
    main()