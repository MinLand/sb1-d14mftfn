from database import db

class Hospital(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    patient_count = db.Column(db.Integer, nullable=False)
    doctors = db.relationship('Doctor', backref='hospital', lazy=True)