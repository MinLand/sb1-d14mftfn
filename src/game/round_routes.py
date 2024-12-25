from flask import Blueprint, jsonify, request
from flask_login import login_required, current_user
from utils.round_manager import RoundManager
from utils.game_state import GameState

bp = Blueprint('round', __name__)

@bp.route('/round/end', methods=['POST'])
@login_required
def end_round():
    game_id = request.form.get('game_id')
    result = RoundManager.end_round(game_id)
    
    if 'error' in result:
        return jsonify(result), 400
        
    return jsonify(result)

@bp.route('/round/state', methods=['GET'])
@login_required
def get_round_state():
    game_id = request.args.get('game_id')
    state = GameState.get_game_state(game_id)
    
    if not state:
        return jsonify({'error': 'Game not found'}), 404
        
    return jsonify(state)