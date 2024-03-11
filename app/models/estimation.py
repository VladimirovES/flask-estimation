from app import db


class Estimation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tester_name = db.Column(db.String(50), nullable=False)
    feature_name = db.Column(db.String(100), nullable=False)
    writing_checks = db.Column(db.Float, nullable=False)
    execution_checks = db.Column(db.Float, nullable=False)
    execution_retests = db.Column(db.Float, nullable=False)
    estimate_testing = db.Column(db.Float, nullable=False)