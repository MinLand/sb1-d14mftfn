from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
import bcrypt
import random
import string
import json

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///game.db'
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Models
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

class Game(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    room_code = db.Column(db.String(6), unique=True)
    player_a = db.Column(db.Integer, db.ForeignKey('user.id'))
    player_d = db.Column(db.Integer, db.ForeignKey('user.id'))
    current_round = db.Column(db.Integer, default=1)
    game_state = db.Column(db.JSON)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

def generate_credentials():
    # Generate 6 character alphanumeric username
    username = ''.join(random.choices(string.ascii_letters + string.digits, k=6))
    # Generate 6 character alphanumeric password
    password = ''.join(random.choices(string.ascii_letters + string.digits, k=6))
    return username, password

@app.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()
        
        if user and bcrypt.checkpw(password.encode('utf-8'), user.password):
            login_user(user)
            return redirect(url_for('dashboard'))
        flash('Invalid username or password')
    return render_template('login.html')

@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')

@app.route('/create_room', methods=['POST'])
@login_required
def create_room():
    role = request.form.get('role')
    room_code = ''.join(random.choices(string.digits, k=6))
    
    game = Game(room_code=room_code)
    if role == 'A':
        game.player_a = current_user.id
    else:
        game.player_d = current_user.id
    
    db.session.add(game)
    db.session.commit()
    
    return jsonify({'room_code': room_code})

@app.route('/join_room', methods=['POST'])
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

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)