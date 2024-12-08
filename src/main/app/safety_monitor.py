from typing import Dict, List, Tuple
import re

class SafetyMonitor:
    def __init__(self):
        self.crisis_patterns = {
            'suicide_risk': [
                r'suicide', r'kill myself', r'end my life', r'better off dead',
                r'want to die', r'don\'t want to live', r'end it all'
            ],
            'self_harm': [
                r'hurt myself', r'harm myself', r'cut myself', r'self[- ]harm',
                r'inflict pain', r'burning myself', r'hitting myself'
            ],
            'abuse': [
                r'abused', r'hitting me', r'threatening me', r'scared of them',
                r'violent', r'trapped', r'controlling me'
            ],
            'emergency': [
                r'right now', r'about to', r'going to', r'have the means',
                r'wrote a note', r'made a plan', r'ready to'
            ]
        }
        
        self.crisis_resources = {
            'suicide_risk': {
                'message': "I'm very concerned about your safety. Please know that you're not alone.",
                'resources': [
                    "988 Suicide & Crisis Lifeline (call or text 988)",
                    "Crisis Text Line (text HOME to 741741)",
                    "Emergency: Call 911"
                ]
            },
            'self_harm': {
                'message': "I hear your pain. Your safety is important.",
                'resources': [
                    "Crisis Text Line (text HOME to 741741)",
                    "Self-harm Crisis Helpline: 1-800-366-8288"
                ]
            },
            'abuse': {
                'message': "Your safety is paramount. There are people who can help.",
                'resources': [
                    "National Domestic Violence Hotline: 1-800-799-SAFE (7233)",
                    "Emergency: Call 911"
                ]
            }
        }

    def analyze_message(self, message: str) -> Dict:
        message = message.lower()
        detected_risks = self._detect_risk_patterns(message)
        
        if not detected_risks:
            return {'risk_level': 'normal', 'risks': []}
            
        risk_assessment = self._assess_risk_level(detected_risks, message)
        response = self._generate_crisis_response(risk_assessment)
        
        return {
            'risk_level': risk_assessment['level'],
            'risks': risk_assessment['detected_risks'],
            'immediate_action': risk_assessment['immediate_action'],
            'response': response
        }

    def _detect_risk_patterns(self, message: str) -> List[Tuple[str, List[str]]]:
        detected = []
        for risk_type, patterns in self.crisis_patterns.items():
            matches = [pattern for pattern in patterns if re.search(pattern, message)]
            if matches:
                detected.append((risk_type, matches))
        return detected

    def _assess_risk_level(self, detected_risks: List[Tuple[str, List[str]]], message: str) -> Dict:
        risk_types = [risk[0] for risk in detected_risks]
        
        # Check for immediate emergency indicators
        immediate_risk = any(pattern in message for pattern in self.crisis_patterns['emergency'])
        
        risk_level = 'high'
        if immediate_risk:
            risk_level = 'severe'
        elif 'suicide_risk' in risk_types:
            risk_level = 'severe'
        elif len(risk_types) > 1:
            risk_level = 'high'
        
        return {
            'level': risk_level,
            'detected_risks': risk_types,
            'immediate_action': immediate_risk
        }

    def _generate_crisis_response(self, risk_assessment: Dict) -> Dict:
        response = {
            'message': "I'm concerned about your wellbeing and safety.",
            'resources': [],
            'actions': []
        }

        for risk_type in risk_assessment['detected_risks']:
            if risk_type in self.crisis_resources:
                crisis_info = self.crisis_resources[risk_type]
                response['message'] = crisis_info['message']
                response['resources'].extend(crisis_info['resources'])

        if risk_assessment['immediate_action']:
            response['actions'].append("IMMEDIATE ACTION REQUIRED: Please call emergency services (911) or reach out to a crisis hotline immediately.")

        return response