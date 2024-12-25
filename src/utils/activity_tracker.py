from typing import Dict, List, Optional
from datetime import datetime
from models.activity import Activity
from models.game import Game
from database import db

class ActivityTracker:
    @staticmethod
    def record_activity(
        game_id: int,
        player_id: int,
        activity_type: str,
        details: Dict,
        cost: int
    ) -> Dict:
        """Record a new player activity"""
        game = Game.query.get(game_id)
        if not game:
            return {'error': 'Game not found'}
            
        activity = Activity(
            game_id=game_id,
            round_number=game.current_round,
            player_id=player_id,
            activity_type=activity_type,
            doctor_id=details.get('doctor_id'),
            topic=details.get('topic'),
            cost=cost,
            created_at=datetime.utcnow()
        )
        
        db.session.add(activity)
        db.session.commit()
        
        return {
            'success': True,
            'activity_id': activity.id
        }
    
    @staticmethod
    def get_round_activities(game_id: int, round_number: int) -> List[Dict]:
        """Get all activities for a specific round"""
        activities = Activity.query.filter_by(
            game_id=game_id,
            round_number=round_number
        ).order_by(Activity.created_at.asc()).all()
        
        return [{
            'id': activity.id,
            'player_id': activity.player_id,
            'type': activity.activity_type,
            'doctor_id': activity.doctor_id,
            'topic': activity.topic,
            'cost': activity.cost,
            'success': activity.success,
            'created_at': activity.created_at.isoformat()
        } for activity in activities]