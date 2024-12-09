from collections import defaultdict
from typing import List, Dict, Any
from datetime import datetime
from .models import ChatMessage

class SessionAnalyzer:
    def __init__(self):
        self.mood_weights = {
            "happy": 1.0,
            "motivated": 0.8,
            "neutral": 0.5,
            "stressed": -0.3,
            "sad": -0.5,
            "depressed": -0.8
        }

    def analyze_mood_trends(self, history: List[ChatMessage]) -> Dict[str, Any]:
        if not history:
            return {"status": "No chat history available"}

        mood_patterns = defaultdict(int)
        mood_progression = []

        for msg in history:
            if msg.mood:
                mood_patterns[msg.mood] += 1
                mood_progression.append({
                    "mood": msg.mood,
                    "timestamp": datetime.now().isoformat(),  # In real implementation, use message timestamp
                    "intensity": self.mood_weights.get(msg.mood, 0)
                })

        return {
            "common_moods": dict(mood_patterns),
            "mood_progression": mood_progression,
            "session_insights": self._analyze_session_patterns(history),
            "suggestions": self._generate_suggestions(mood_patterns)
        }

    def _analyze_session_patterns(self, history: List[ChatMessage]) -> Dict[str, Any]:
        patterns = {
            "total_messages": len(history),
            "response_patterns": self._analyze_response_patterns(history),
            "engagement_level": self._calculate_engagement(history)
        }
        return patterns

    def _analyze_response_patterns(self, history: List[ChatMessage]) -> Dict[str, Any]:
        message_lengths = [len(msg.content) for msg in history]
        return {
            "avg_message_length": sum(message_lengths) / len(message_lengths) if message_lengths else 0,
            "total_interactions": len(history)
        }

    def _calculate_engagement(self, history: List[ChatMessage]) -> str:
        avg_length = self._analyze_response_patterns(history)["avg_message_length"]
        if avg_length > 100:
            return "high"
        elif avg_length > 50:
            return "medium"
        return "low"

    def _generate_suggestions(self, mood_patterns: Dict[str, int]) -> List[str]:
        suggestions = []
        if not mood_patterns:
            return ["Start tracking your moods to get personalized suggestions"]

        most_common_mood = max(mood_patterns.items(), key=lambda x: x[1])[0]
        
        suggestions_map = {
            "stressed": [
                "Consider trying breathing exercises",
                "Take short breaks between tasks",
                "Practice mindfulness meditation"
            ],
            "sad": [
                "Engage in activities you enjoy",
                "Connect with supportive people",
                "Set small, achievable goals"
            ],
            "depressed": [
                "Consider professional support",
                "Maintain daily routines",
                "Set gentle self-care goals"
            ]
        }

        return suggestions_map.get(most_common_mood, ["Track more moods for personalized suggestions"])