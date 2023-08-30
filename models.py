# models.py

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Integer, String, DateTime
from sqlalchemy.dialects.postgresql import JSON  # Import JSON

db = SQLAlchemy()

class FAQ(db.Model):
    __tablename__ = 'faq'

    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.String, nullable=True)
    answer = db.Column(db.String, nullable=True)
    question_embedding = db.Column(JSON, nullable=True)  # Use JSON to store the list of floats
    question_length = db.Column(db.Integer, nullable=True)
    question_tokens = db.Column(db.Integer, nullable=True)
    enable_flag = db.Column(db.Integer, nullable=True)
    created_at = db.Column(db.DateTime, nullable=True)
    updated_at = db.Column(db.DateTime, nullable=True)
