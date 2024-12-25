from typing import Dict, List
from models.activity import Activity
from models.doctor import Doctor
from datetime import datetime, timedelta

class MarketTrends:
    @staticmethod
    def calculate_trend(game_id: int, rounds: int = 3) -> Dict[str, List[float]]:
        """Calculate market share trends over the last N rounds"""
        current_round = Activity.query.filter_by(game_id=game_id).order_by(
            Activity.round_number.desc()
        ).first().round_number
        
        start_round = max(1, current_round - rounds + 1)
        trends = {
            'A': [],
            'D': [],
            'generic': []
        }
        
        for round_num in range(start_round, current_round + 1):
            shares = MarketTrends._calculate_round_shares(game_id, round_num)
            trends['A'].append(shares['A'])
            trends['D'].append(shares['D'])
            trends['generic'].append(shares['generic'])
            
        return trends
    
    @staticmethod
    def _calculate_round_shares(game_id: int, round_num: int) -> Dict[str, float]:
        """Calculate market shares for a specific round"""
        doctors = Doctor.query.all()
        total_rx = 0
        a_rx = 0
        d_rx = 0
        
        for doctor in doctors:
            total = doctor.a_drug + doctor.d_drug + doctor.generic
            total_rx += total
            a_rx += doctor.a_drug
            d_rx += doctor.d_drug
            
        if total_rx == 0:
            return {'A': 0, 'D': 0, 'generic': 0}
            
        return {
            'A': (a_rx / total_rx) * 100,
            'D': (d_rx / total_rx) * 100,
            'generic': ((total_rx - a_rx - d_rx) / total_rx) * 100
        }