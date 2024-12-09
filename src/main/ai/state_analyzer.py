from typing import Dict, List
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
            'neutral': [
                r'hello', r'hi', r'hey', r'how are you',
                r'good morning', r'good afternoon', r'good evening'
            ],
            'anxiety': [
                r'anxious', r'worried', r'panic', r'stress',
                r'overwhelm', r'nervous', r'fear', r'tension'
            ],
            'depression': [
                r'depress', r'sad', r'hopeless', r'worthless',
                r'tired', r'exhausted', r'empty', r'lonely'
            ],
            'anger': [
                r'angry', r'furious', r'rage', r'frustrated',
                r'irritated', r'mad', r'resent'
            ],
            'grief': [
                r'loss', r'grief', r'miss', r'gone',
                r'death', r'passed away', r'mourning'
            ],
            'relationship': [
                r'relationship', r'partner', r'marriage',
                r'divorce', r'family', r'friend', r'conflict'
            ],
            'trauma': [
                r'trauma', r'abuse', r'ptsd', r'flashback',
                r'nightmare', r'trigger', r'assault'
            ],
            'self_esteem': [
                r'confidence', r'self-worth', r'ugly',
                r'failure', r'not good enough', r'shame'
            ],
            'crisis': [
                r'suicide', r'kill myself', r'better off dead',
                r'end it all', r'no point living', r'harm myself'
            ]
        }
        
        self.intensity_modifiers = [
            (r'very|really|extremely|completely|always', 0.3),
            (r'quite|rather|fairly|often', 0.2),
            (r'sometimes|occasionally|a bit|slightly', -0.1),
            (r'maybe|perhaps|not sure', -0.2)
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
            
        # Default to neutral if no strong emotions detected
        max_emotion = max(emotion_scores.items(), key=lambda x: x[1])
        return max_emotion[0] if max_emotion[1] > 0 else 'neutral'
    
    def _calculate_intensity(self, message: str) -> float:
        # For neutral messages, return low intensity
        if self._detect_primary_emotion(message) == 'neutral':
            return 0.1
            
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
        """Determine appropriate response type based on emotional state"""
        if state.risk_level > 0.7:
            return 'crisis_intervention'
        elif state.intensity > 0.8:
            return 'grounding'
        elif state.intensity > 0.6:
            return 'emotional_support'
        elif state.primary_emotion == 'neutral':
            return 'rapport_building'
        else:
            return 'therapeutic_exploration'