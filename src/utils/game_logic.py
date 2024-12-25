import random
import string
from models.game import Game
from models.activity import Activity
from models.doctor import Doctor

class GameLogic:
    @staticmethod
    def generate_room_code():
        return ''.join(random.choices(string.digits, k=6))
        
    @staticmethod
    def process_visit(game_id, user_id, doctor_id, topic):
        game = Game.query.get(game_id)
        if not game:
            return {'error': 'Game not found'}
            
        # Check action points and budget
        if not GameLogic.can_perform_action(game, user_id, 300):
            return {'error': 'Insufficient resources'}
            
        # Process visit logic
        doctor = Doctor.query.get(doctor_id)
        feedback = GameLogic.calculate_visit_feedback(doctor, topic)
        
        # Record activity
        activity = Activity(
            game_id=game_id,
            round_number=game.current_round,
            player_id=user_id,
            activity_type='visit',
            doctor_id=doctor_id,
            topic=topic,
            cost=300
        )
        
        db.session.add(activity)
        db.session.commit()
        
        return {'success': True, 'feedback': feedback}
        
    @staticmethod
    def can_perform_action(game, user_id, cost):
        is_player_a = user_id == game.player_a
        
        if is_player_a:
            return game.actions_a > 0 and game.budget_a >= cost
        else:
            return game.actions_d > 0 and game.budget_d >= cost