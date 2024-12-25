from typing import Dict, Optional
from models.game import Game
from models.activity import Activity
from database import db

class GameState:
    @staticmethod
    def initialize_round(game_id: int) -> Dict:
        """Initialize a new round for the game"""
        game = Game.query.get(game_id)
        if not game:
            return {'error': 'Game not found'}
            
        game.actions_a = 4
        game.actions_d = 3
        game.budget_a = 60000
        game.budget_d = 60000
        game.current_round += 1
        
        db.session.commit()
        return {
            'round': game.current_round,
            'budget_a': game.budget_a,
            'budget_d': game.budget_d,
            'actions_a': game.actions_a,
            'actions_d': game.actions_d
        }
    
    @staticmethod
    def get_game_state(game_id: int) -> Optional[Dict]:
        """Get current game state"""
        game = Game.query.get(game_id)
        if not game:
            return None
            
        return {
            'round': game.current_round,
            'budget_a': game.budget_a,
            'budget_d': game.budget_d,
            'actions_a': game.actions_a,
            'actions_d': game.actions_d,
            'player_a': game.player_a,
            'player_d': game.player_d
        }