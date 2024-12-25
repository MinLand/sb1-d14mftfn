from models.activity import Activity
from models.doctor import Doctor
from database import db

class GameLogic:
    @staticmethod
    def calculate_topic_match(doctor_id, topic, company):
        doctor = Doctor.query.get(doctor_id)
        if not doctor:
            return 0
        
        # Calculate match score based on doctor's learning preferences
        score = 0
        if topic in doctor.learn_high:
            score += 2
        elif topic in doctor.learn_low:
            score += 1
            
        return score

    @staticmethod
    def resolve_speaker_conflict(game_id, round_number, doctor_id):
        activities = Activity.query.filter_by(
            game_id=game_id,
            round_number=round_number,
            doctor_id=doctor_id
        ).all()
        
        if len(activities) <= 1:
            return
            
        # Calculate match scores
        scores = {}
        for activity in activities:
            scores[activity.id] = GameLogic.calculate_topic_match(
                doctor_id, 
                activity.topic, 
                'A' if activity.player_id == game.player_a else 'D'
            )
            
        # Find highest score
        max_score = max(scores.values())
        winners = [k for k, v in scores.items() if v == max_score]
        
        # If tie, use market share
        if len(winners) > 1:
            # TODO: Implement market share comparison
            winner = winners[0]
        else:
            winner = winners[0]
            
        # Mark other activities as failed
        for activity in activities:
            if activity.id != winner:
                activity.success = False
                
        db.session.commit()