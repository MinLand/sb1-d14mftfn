from models.hospital import Hospital
from models.doctor import Doctor

class MarketResearch:
    @staticmethod
    def get_hospital_stats(game_id):
        hospitals = Hospital.query.all()
        stats = []
        
        for hospital in hospitals:
            bio_usage = 0  # Calculate from game state
            a_share = 0    # Calculate from game state
            d_share = 0    # Calculate from game state
            
            stats.append({
                'name': hospital.name,
                'potential': hospital.patient_count,
                'bio_usage': bio_usage,
                'a_share': a_share,
                'd_share': d_share
            })
            
        return stats

    @staticmethod
    def get_market_shares(game_id):
        return {
            'a_drug': 0,  # Calculate from game state
            'd_drug': 0,  # Calculate from game state
            'generic': 0  # Calculate from game state
        }