from flask import Blueprint, jsonify, request
from flask_login import login_required, current_user
from models.hospital import Hospital
from models.doctor import Doctor
from models.game import Game
from utils.market_research import MarketResearch

bp = Blueprint('api', __name__)

@bp.route('/api/hospitals')
@login_required
def get_hospitals():
    hospitals = Hospital.query.all()
    return jsonify([{
        'id': h.id,
        'name': h.name,
        'patient_count': h.patient_count
    } for h in hospitals])

@bp.route('/api/doctors/<int:hospital_id>')
@login_required
def get_doctors(hospital_id):
    doctors = Doctor.query.filter_by(hospital_id=hospital_id).all()
    return jsonify([{
        'id': d.id,
        'name': d.name,
        'knowledge_a': d.knowledge_a,
        'knowledge_d': d.knowledge_d,
        'knowledge_generic': d.knowledge_generic
    } for d in doctors])

@bp.route('/api/research', methods=['POST'])
@login_required
def conduct_research():
    game = Game.query.filter_by(
        player_a=current_user.id if current_user.is_player_a else None,
        player_d=current_user.id if not current_user.is_player_a else None
    ).first()
    
    if not game:
        return jsonify({'error': 'Game not found'}), 404
        
    hospital_stats = MarketResearch.get_hospital_stats(game.id)
    market_shares = MarketResearch.get_market_shares(game.id)
    
    return jsonify({
        'hospital_stats': hospital_stats,
        'market_shares': market_shares
    })