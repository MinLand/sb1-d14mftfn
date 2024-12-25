from typing import Dict
from models.game import Game
from models.activity import Activity
from utils.game_state import GameState
from utils.market_research import MarketResearch
from database import db

class RoundManager:
    @staticmethod
    def end_round(game_id: int) -> Dict:
        """Process end of round and return updated state"""
        game = Game.query.get(game_id)
        if not game:
            return {'error': 'Game not found'}
            
        # Calculate round results
        market_data = MarketResearch.get_market_overview(game_id)
        
        # Store round results
        game.game_state = {
            'round': game.current_round,
            'market_data': market_data
        }
        
        # Check if game is complete
        if game.current_round >= 15:
            return RoundManager._end_game(game_id)
            
        # Initialize next round
        new_state = GameState.initialize_round(game_id)
        
        return {
            'round_complete': True,
            'market_data': market_data,
            'next_round': new_state
        }
    
    @staticmethod
    def _end_game(game_id: int) -> Dict:
        """Process end of game and calculate final results"""
        market_data = MarketResearch.get_market_overview(game_id)
        
        return {
            'game_complete': True,
            'final_market_data': market_data
        }