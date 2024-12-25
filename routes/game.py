from flask import Blueprint, jsonify, request
from flask_login import login_required, current_user
from models.game import Game
from models.activity import Activity
from utils.game_logic import GameLogic
from utils.market_research import MarketResearch
from database import db

bp = Blueprint('game', __name__)

@bp.route('/game/<game_id>/visit', methods=['POST'])
@login_required
def academic_visit():
    doctor_id = request.form.get('doctor_id')
    topic = request.form.get('topic')
    game_id = request.form.get('game_id')
    
    game = Game.query.get(game_id)
    if not game:
        return jsonify({'error': 'Game not found'}), 404
        
    # Check action points and budget
    if current_user.id == game.player_a:
        if game.actions_a <= 0:
            return jsonify({'error': 'No actions left'}), 400
        if game.budget_a < 300:
            return jsonify({'error': 'Insufficient funds'}), 400
        game.actions_a -= 1
        game.budget_a -= 300
    else:
        if game.actions_d <= 0:
            return jsonify({'error': 'No actions left'}), 400
        if game.budget_d < 300:
            return jsonify({'error': 'Insufficient funds'}), 400
        game.actions_d -= 1
        game.budget_d -= 300
    
    activity = Activity(
        game_id=game_id,
        round_number=game.current_round,
        player_id=current_user.id,
        activity_type='visit',
        doctor_id=doctor_id,
        topic=topic,
        cost=300
    )
    
    db.session.add(activity)
    db.session.commit()
    
    return jsonify({'success': True})

@bp.route('/game/<game_id>/research', methods=['POST'])
@login_required
def market_research():
    game_id = request.form.get('game_id')
    game = Game.query.get(game_id)
    
    if not game:
        return jsonify({'error': 'Game not found'}), 404
        
    # Check action points and budget
    if current_user.id == game.player_a:
        if game.actions_a <= 0:
            return jsonify({'error': 'No actions left'}), 400
        if game.budget_a < 1000:
            return jsonify({'error': 'Insufficient funds'}), 400
        game.actions_a -= 1
        game.budget_a -= 1000
    else:
        if game.actions_d <= 0:
            return jsonify({'error': 'No actions left'}), 400
        if game.budget_d < 1000:
            return jsonify({'error': 'Insufficient funds'}), 400
        game.actions_d -= 1
        game.budget_d -= 1000
    
    hospital_stats = MarketResearch.get_hospital_stats(game_id)
    market_shares = MarketResearch.get_market_shares(game_id)
    
    db.session.commit()
    
    return jsonify({
        'hospital_stats': hospital_stats,
        'market_shares': market_shares
    })