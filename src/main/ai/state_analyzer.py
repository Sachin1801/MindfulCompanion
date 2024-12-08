from typing import Dict, List, Optional
import re
from dataclasses import dataclass
from datetime import datetime

@dataclass
class EmotionalState:
    primary_emotion: str
    intensity: float  # 0-1 scale
    risk_level: float  # 0-1 scale
    timestamp: datetime

class StateAnalyzer:
    def __init__(self):
        self.emotion_patterns = {
            'depression': [
                r'worthless', r'nothing but', r'never get around',
                r'barely sleep', r'don\'t deserve', r'given up'
            ],
            'anxiety': [
                r'can\'t stop', r'constantly', r'overwhelming',
                r'never ends', r'worried sick', r'panic'
            ],
            'crisis': [
                r'suicide', r'kill myself', r'better off dead',
                r'end it all', r'no point living'
            ]
        }
        
        self.intensity_modifiers = [
            (r'very|really|extremely|completely', 0.3),
            (r'always|never|constantly', 0.2),
            (r'sometimes|occasionally', -0.1),
            (r'maybe|perhaps', -0.2)
        ]
        
    def analyze_message(self, message: str) -> EmotionalState:
        message = message.lower()
        primary_emotion = self._detect_primary_emotion(message)
        intensity = self._calculate_intensity(message)
        risk_level = self._assess_risk(message, primary_emotion, intensity)
        
        return EmotionalState(
            primary_emotion=primary_emotion,
            intensity=intensity,
            risk_level=risk_level,
            timestamp=datetime.now()
        )
    
    def _detect_primary_emotion(self, message: str) -> str:
        emotion_scores = {}
        
        for emotion, patterns in self.emotion_patterns.items():
            score = sum(len(re.findall(pattern, message)) for pattern in patterns)
            emotion_scores[emotion] = score
            
        return max(emotion_scores.items(), key=lambda x: x[1])[0]
    
    def _calculate_intensity(self, message: str) -> float:
        base_intensity = 0.5
        
        for pattern, modifier in self.intensity_modifiers:
            if re.search(pattern, message):
                base_intensity = min(1.0, max(0.0, base_intensity + modifier))
                
        return base_intensity
    
    def _assess_risk(self, message: str, emotion: str, intensity: float) -> float:
        risk_level = 0.0
        
        # Base risk on emotion type
        if emotion == 'crisis':
            risk_level = 0.8
        elif emotion == 'depression':
            risk_level = 0.4
        elif emotion == 'anxiety':
            risk_level = 0.3
            
        # Adjust risk based on intensity
        risk_level = min(1.0, risk_level + (intensity * 0.2))
        
        # Check for immediate risk patterns
        immediate_risk_patterns = [
            r'right now', r'tonight', r'plan to',
            r'going to', r'decided to'
        ]
        
        if any(re.search(pattern, message) for pattern in immediate_risk_patterns):
            risk_level = min(1.0, risk_level + 0.3)
            
        return risk_level

    def get_response_type(self, state: EmotionalState) -> str:
        if state.risk_level > 0.7:
            return 'crisis'
        elif state.risk_level > 0.5:
            return 'urgent'
        elif state.intensity > 0.7:
            return 'grounding'
        else:
            return 'supportive'