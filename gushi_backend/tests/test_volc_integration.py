"""
VolcEngine AI Service Test Script
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ai_services.ai_client import get_ai_response, test_ai_connection
from config import Config

def test_volc_integration():
    """Test VolcEngine integration"""
    print("=== VolcEngine AI Service Test ===")
    
    # Check if VolcEngine API key is configured
    if not Config.VOLC_API_KEY:
        print("❌ VolcEngine API key not configured")
        print("   Please set VOLC_API_KEY in .env file")
        return
    
    print(f"✅ VolcEngine API key configured")
    print(f"   Model name: {Config.VOLC_MODEL_NAME or 'Not configured'}")
    print(f"   API URL: {Config.VOLC_BASE_URL}")
    
    # Test connection
    print("\n--- Testing connection ---")
    try:
        result = test_ai_connection('volc')
        if result['success']:
            print("✅ VolcEngine connection test successful")
            print(f"   Response length: {result['response_length']}")
            print(f"   Sample response: {result['sample_response']}")
        else:
            print("❌ VolcEngine connection test failed")
            print(f"   Error: {result['error']}")
    except Exception as e:
        print("❌ VolcEngine connection test exception")
        print(f"   Exception: {str(e)}")
    
    # Test specific call
    print("\n--- Testing specific call ---")
    try:
        test_prompt = "Please briefly introduce the application of artificial intelligence in financial investment, no more than 50 words."
        response = get_ai_response(test_prompt, 'volc', max_tokens=100)
        print("✅ VolcEngine call test successful")
        print(f"   Response: {response}")
        print(f"   Response length: {len(response)}")
    except Exception as e:
        print("❌ VolcEngine call test failed")
        print(f"   Error: {str(e)}")

def test_model_selection():
    """Test model selection"""
    print("\n=== Model Selection Test ===")
    
    models_to_test = [
        Config.VOLC_MODEL_NAME,
        "doubao-pro-32k",
        "doubao-pro-128k"
    ]
    
    for model_name in models_to_test:
        if not model_name:
            continue
            
        print(f"\n--- Testing model: {model_name} ---")
        try:
            response = get_ai_response(
                "Hello, please introduce yourself.",
                'volc',
                model_name=model_name,
                max_tokens=50
            )
            print(f"✅ Model {model_name} call successful")
            print(f"   Response: {response[:50]}...")
        except Exception as e:
            print(f"❌ Model {model_name} call failed: {str(e)}")

if __name__ == "__main__":
    test_volc_integration()
    test_model_selection()
    print("\n=== VolcEngine Integration Test Completed ===")