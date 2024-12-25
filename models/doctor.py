from database import db

class Doctor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    hospital_id = db.Column(db.Integer, db.ForeignKey('hospital.id'))
    knowledge_a = db.Column(db.Integer, default=0)
    knowledge_d = db.Column(db.Integer, default=0)
    knowledge_generic = db.Column(db.Integer, default=0)
    learn_low = db.Column(db.JSON)  # List of topics
    learn_high = db.Column(db.JSON)  # List of topics
    event_no = db.Column(db.JSON)   # List of events
    event_low = db.Column(db.JSON)  # List of events
    event_high = db.Column(db.JSON) # List of events
    decision_weight = db.Column(db.Float)