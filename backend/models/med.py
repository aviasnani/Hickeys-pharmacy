from flask_login import UserMixin
from . import db

class Meds(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    brand = db.Column(db.String(20), nullable=False)
    description = db.Column(db.String(200), nullable=False)
    form = db.Column(db.String(20), nullable=False) # form of the medicine (tablet, syrup, etc.)
    dosage = db.Column(db.String(20), nullable=False)
    price = db.Column(db.Float, nullable=False)