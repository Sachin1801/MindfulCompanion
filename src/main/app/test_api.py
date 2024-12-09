import requests
import json
from typing import Dict, Any
import time
from datetime import datetime

class APITester:
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url
        self.user_id = None
        self.headers = {"Content-Type": "application/json"}
        print(f"🚀 Starting API tests at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    def run_all_tests(self):
        """Run all API tests in sequence"""
        try:
            self.test_profile_creation()
            self.test_basic_chat()
            self.test_emotional_scenarios()
            self.test_crisis_detection()
            self.test_conversation_context()
            self.test_history_retrieval()
            self.test_mood_analysis()
            print("\n✅ All tests completed successfully!")
        except Exception as e:
            print(f"\n❌ Test suite failed: {str(e)}")

    def make_request(self, method: str, endpoint: str, data: Dict[str, Any] = None) -> Dict:
        """Make HTTP request and handle response"""
        url = f"{self.base_url}/{endpoint}"
        try:
            if method.upper() == "GET":
                response = requests.get(url, headers=self.headers)
            else:
                response = requests.post(url, headers=self.headers, json=data)
            
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"❌ Request failed: {str(e)}")
            if hasattr(e.response, 'json'):
                print(f"Response: {e.response.json()}")
            raise

    def test_profile_creation(self):
        """Test user profile creation"""
        print("\n📋 Testing Profile Creation...")
        profile_data = {
            "name": "Test User",
            "age_category": "20-40",
            "emotions": ["anxiety", "stress"],
            "therapy_status": "considering",
            "interaction_style": "gentle",
            "stress_level": "moderate",
            "goals": "Better stress management"
        }
        
        response = self.make_request("POST", "profile", profile_data)
        print("✅ Profile created successfully")
        return response

    def test_basic_chat(self):
        """Test basic chat functionality"""
        print("\n💭 Testing Basic Chat...")
        messages = [
            {"message": "Hello, how are you?", "mood": "neutral"},
            {"message": "What kind of support can you provide?", "mood": "neutral"}
        ]
        
        for msg in messages:
            response = self.make_request("POST", "chat", msg)
            print(f"✅ Chat response received for: '{msg['message']}'")
            time.sleep(1)  # Prevent rate limiting

    def test_emotional_scenarios(self):
        """Test various emotional scenarios"""
        print("\n🎭 Testing Emotional Scenarios...")
        scenarios = [
            {"message": "I'm feeling really happy today", "mood": "happy"},
            {"message": "Work is stressing me out", "mood": "stressed"},
            {"message": "I accomplished my goal today", "mood": "motivated"},
            {"message": "I'm feeling a bit down", "mood": "sad"}
        ]
        
        for scenario in scenarios:
            response = self.make_request("POST", "chat", scenario)
            print(f"✅ Tested emotional scenario: {scenario['mood']}")
            time.sleep(1)

    def test_crisis_detection(self):
        """Test crisis detection system"""
        print("\n⚠️ Testing Crisis Detection...")
        crisis_messages = [
            {"message": "I'm feeling overwhelmed but managing", "mood": "stressed"},
            {"message": "Everything feels too much to handle", "mood": "depressed"}
        ]
        
        for msg in crisis_messages:
            response = self.make_request("POST", "chat", msg)
            print(f"✅ Crisis detection tested for: '{msg['message']}'")
            time.sleep(1)

    def test_conversation_context(self):
        """Test conversation context maintenance"""
        print("\n🧩 Testing Conversation Context...")
        context_messages = [
            {"message": "I've been having trouble at work", "mood": "stressed"},
            {"message": "My boss is giving me impossible deadlines", "mood": "stressed"},
            {"message": "I tried talking to HR about it", "mood": "neutral"}
        ]
        
        for msg in context_messages:
            response = self.make_request("POST", "chat", msg)
            print(f"✅ Context message processed: '{msg['message']}'")
            time.sleep(1)

    def test_history_retrieval(self):
        """Test chat history retrieval"""
        print("\n📜 Testing History Retrieval...")
        response = self.make_request("GET", "history")
        print(f"✅ Successfully retrieved chat history")
        return response

    def test_mood_analysis(self):
        """Test mood analysis functionality"""
        print("\n📊 Testing Mood Analysis...")
        response = self.make_request("GET", "analysis/mood")
        print(f"✅ Successfully retrieved mood analysis")
        return response

if __name__ == "__main__":
    tester = APITester()
    tester.run_all_tests()