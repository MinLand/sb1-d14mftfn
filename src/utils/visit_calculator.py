from models.doctor import Doctor
from utils.doctor_data import DOCTOR_DATA
from utils.topic_data import COMPANY_A_TOPICS, COMPANY_D_TOPICS

class VisitCalculator:
    @staticmethod
    def calculate_visit_impact(doctor_name: str, topic: str, company: str) -> dict:
        doctor_data = DOCTOR_DATA[doctor_name]
        topics = COMPANY_A_TOPICS if company == 'A' else COMPANY_D_TOPICS
        topic_data = topics[topic]
        
        # Calculate impact based on learning preferences
        impact = 0
        for characteristic in topic_data["characteristics"]:
            if characteristic in doctor_data.learn_high:
                impact += 2
            elif characteristic in doctor_data.learn_low:
                impact += 1
                
        return {
            "impact": impact,
            "knowledge_increase": impact * 10,
            "feedback": VisitCalculator.generate_feedback(impact, doctor_name, topic)
        }
    
    @staticmethod
    def generate_feedback(impact: int, doctor_name: str, topic: str) -> str:
        if impact >= 2:
            return f"{doctor_name}对{topic}表现出很大兴趣，并详细询问了相关数据。"
        elif impact == 1:
            return f"{doctor_name}听取了{topic}的介绍，表示理解。"
        else:
            return f"{doctor_name}简单听取了{topic}的介绍。"