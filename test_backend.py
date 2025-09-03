import requests
import json

def test_backend():
    """Test the FastAPI backend endpoints"""
    
    base_url = "http://localhost:8000"
    
    print("🧪 Testing DeepVision Research API Backend...")
    print("=" * 50)
    
    # Test health endpoint
    try:
        print("1. Testing health endpoint...")
        response = requests.get(f"{base_url}/api/health")
        if response.status_code == 200:
            print("   ✅ Health check passed")
            print(f"   Response: {response.json()}")
        else:
            print(f"   ❌ Health check failed: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("   ❌ Cannot connect to backend. Is it running?")
        return False
    except Exception as e:
        print(f"   ❌ Health check error: {e}")
        return False
    
    # Test research endpoint with a simple query
    try:
        print("\n2. Testing research endpoint...")
        test_query = {
            "query": "What is artificial intelligence?",
            "num_reflections": 1,
            "num_results_per_search": 2,
            "cap_search_length": 10000
        }
        
        print(f"   Sending query: {test_query['query']}")
        response = requests.post(
            f"{base_url}/api/research",
            json=test_query,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            data = response.json()
            print("   ✅ Research endpoint working")
            print(f"   Status: {data.get('status')}")
            print(f"   Message: {data.get('message')}")
            
            if data.get('progress'):
                progress = data['progress']
                print(f"   Total sections: {progress.get('total_sections', 'N/A')}")
                print(f"   Reflections per section: {progress.get('reflections_per_section', 'N/A')}")
            
            if data.get('final_report'):
                print(f"   Final report length: {len(data['final_report'])} characters")
                print("   Report preview:")
                print("   " + data['final_report'][:200] + "...")
            
        else:
            print(f"   ❌ Research endpoint failed: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"   ❌ Research endpoint error: {e}")
        return False
    
    print("\n" + "=" * 50)
    print("🎉 All tests passed! Backend is working correctly.")
    return True

if __name__ == "__main__":
    success = test_backend()
    if not success:
        print("\n❌ Some tests failed. Check the backend logs for details.")
        exit(1)
