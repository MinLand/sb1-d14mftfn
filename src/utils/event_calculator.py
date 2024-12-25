from typing import List
from models.doctor import Doctor
from utils.doctor_data import DOCTOR_DATA

class EventCalculator:
    @staticmethod
    def calculate_event_impact(doctor_name: str, event_type: str, role: str) -> dict:
        doctor_data = DOCTOR_DATA[doctor_name]
        
        # Calculate impact based on event preferences
        impact = 0
        if event_type in doctor_data.event_high:
            impact = 3
        elif event_type in doctor_data.event_low:
            impact = 1
        elif event_type in doctor_data.event_no:
            impact = 0
            
        return {
            "impact": impact,
            "knowledge_increase": impact * 15,
            "success": impact > 0
        }
    
    @staticmethod
    def resolve_speaker_conflict(doctor_name: str, company_a_topic: str, company_d_topic: str) -> str:
        doctor_data = DOCTOR_DATA[doctor_name]
        impact_a = EventCalculator.calculate_event_impact(doctor_name, company_a_topic, 'A')
        impact_d = EventCalculator.calculate_event_impact(doctor_name, company_d_topic, 'D')
        
        if impact_a["impact"] > impact_d["impact"]:
            return 'A'
        elif impact_d["impact"] > impact_a["impact"]:
            return 'D'
        else:
            # If equal impact, use market share or other criteria
            return 'A'  # Placeholder logic