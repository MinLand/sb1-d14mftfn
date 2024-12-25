from typing import Dict, List
from models.hospital import Hospital
from models.doctor import Doctor
from utils.hospital_stats import HospitalStats
from utils.market_trends import MarketTrends

class MarketResearch:
    @staticmethod
    def get_hospital_stats(game_id: int) -> List[Dict]:
        """Get comprehensive statistics for all hospitals"""
        hospitals = Hospital.query.all()
        stats = []
        
        for hospital in hospitals:
            stats.append({
                'name': hospital.name,
                'potential': hospital.patient_count,
                'bio_usage': HospitalStats.calculate_bio_usage(hospital.id, game_id),
                'a_share': HospitalStats.calculate_market_share(hospital.id, game_id, 'A'),
                'd_share': HospitalStats.calculate_market_share(hospital.id, game_id, 'D')
            })
            
        return stats

    @staticmethod
    def get_market_overview(game_id: int) -> Dict:
        """Get overall market overview including trends"""
        trends = MarketTrends.calculate_trend(game_id)
        current_shares = trends['A'][-1], trends['D'][-1], trends['generic'][-1]
        
        return {
            'current_shares': {
                'a_drug': current_shares[0],
                'd_drug': current_shares[1],
                'generic': current_shares[2]
            },
            'trends': trends
        }