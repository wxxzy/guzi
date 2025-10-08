import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ai_services.ai_client import get_ai_response, test_ai_connection

def main():
    print("Testing Volc Engine AI Service...")
    
    # Test connection
    try:
        result = test_ai_connection('volc')
        print("Connection test:", "SUCCESS" if result['success'] else "FAILED")
        if result['success']:
            print("Response length:", result['response_length'])
    except Exception as e:
        print("Connection test failed:", str(e))
        return
    
    # Test specific call
    try:
        response = get_ai_response(
            "Please introduce artificial intelligence in one sentence.",
            'volc',
            max_tokens=50
        )
        print("Specific call test: SUCCESS")
        print("Response:", response[:100])
    except Exception as e:
        print("Specific call test failed:", str(e))

if __name__ == "__main__":
    main()