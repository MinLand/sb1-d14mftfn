from flask import Blueprint, jsonify, request
from flask_login import login_required, current_user
from models.game import Game
from models.activity import Activity
from utils.game_logic import GameLogic
from utils.market_research import MarketResearch

bp = Blueprint('actions', __name__)

@bp.route('/action/visit', methods=['POST'])
@login_required
def academic_visit():
    doctor_id = request.form.get('doctor_id')
    topic = request.form.get('topic')
    game_id = request.form.get('game_id')
    
    result = GameLogic.process_visit(game_id, current_user.id, doctor_id, topic)
    if 'error' in result:
        return jsonify(result), 400
        
    return jsonify({'success': True, 'feedback': result['feedback']})

@bp.route('/action/research', methods=['POST'])
@login_required
def market_research():
    game_id = request.form.get('game_id')
    
    result = GameLogic.process_research(game_id, current_user.id)
    if 'error' in result:
        return jsonify(result), 400
        
    return jsonify(result)