from database import db
from datetime import datetime

class Activity(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    game_id = db.Column(db.Integer, db.ForeignKey('game.id'))
    round_number = db.Column(db.Integer, nullable=False)
    player_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    activity_type = db.Column(db.String(50), nullable=False)  # visit, city_meeting, conference, research
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctor.id'))
    topic = db.Column(db.String(100))
    cost = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    success = db.Column(db.Boolean, default=True)