from database import db

class Game(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    room_code = db.Column(db.String(6), unique=True)
    player_a = db.Column(db.Integer, db.ForeignKey('user.id'))
    player_d = db.Column(db.Integer, db.ForeignKey('user.id'))
    current_round = db.Column(db.Integer, default=1)
    game_state = db.Column(db.JSON)
    budget_a = db.Column(db.Integer, default=60000)
    budget_d = db.Column(db.Integer, default=60000)
    actions_a = db.Column(db.Integer, default=4)
    actions_d = db.Column(db.Integer, default=3)