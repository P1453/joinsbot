from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.types import TypeDecorator, TEXT

class Vector(TypeDecorator):
    impl = TEXT

    def process_bind_param(self, value, dialect):
        return str(value)  # ここでvalueを適切に変換してください。

    def process_result_value(self, value, dialect):
        return value  # ここでvalueを適切に変換してください。

db = SQLAlchemy()

class FAQ(db.Model):
    __tablename__ = 'faq'

    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.Text, nullable=True)
    answer = db.Column(db.Text, nullable=True)
    question_embedding = db.Column(Vector, nullable=True)  # Use the custom Vector type
    question_length = db.Column(db.Integer, nullable=True)
    question_tokens = db.Column(db.Integer, nullable=True)
    enable_flag = db.Column(db.Integer, nullable=True)
    created_at = db.Column(db.DateTime, nullable=True)
    updated_at = db.Column(db.DateTime, nullable=True)
