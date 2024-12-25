from flask import Blueprint, render_template, jsonify, request
from flask_login import login_required, current_user
from models.game import Game
from utils.game_logic import GameLogic

bp = Blueprint('game', __name__)

@bp.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')

@bp.route('/create_room', methods=['POST'])
@login_required
def create_room():
    role = request.form.get('role')
    room_code = GameLogic.generate_room_code()
    
    game = Game(room_code=room_code)
    if role == 'A':
        game.player_a = current_user.id
    else:
        game.player_d = current_user.id
    
    db.session.add(game)
    db.session.commit()
    
    return jsonify({'room_code': room_code})

@bp.route('/join_room', methods=['POST'])
@login_required
def join_room():
    room_code = request.form.get('room_code')
    game = Game.query.filter_by(room_code=room_code).first()
    
    if not game:
        return jsonify({'error': 'Room not found'}), 404
        
    if game.player_a and game.player_d:
        return jsonify({'error': 'Room is full'}), 400
        
    if not game.player_a:
        game.player_a = current_user.id
    else:
        game.player_d = current_user.id
    
    db.session.commit()
    return jsonify({'success': True})