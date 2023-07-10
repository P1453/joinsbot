# app.py

from flask import Flask, render_template, request, redirect, url_for, abort, jsonify  # add jsonify
from flask_migrate import Migrate
from models import db, FAQ
from config import SQLALCHEMY_DATABASE_URI, SQLALCHEMY_TRACK_MODIFICATIONS
from datetime import datetime
from sqlalchemy import create_engine, text
import numpy as np
import openai
import os
from dotenv import load_dotenv

load_dotenv('local.env')
os.environ.get('OPENAI_API_KEY')



app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = SQLALCHEMY_TRACK_MODIFICATIONS

db.init_app(app)
migrate = Migrate(app, db)




engine = create_engine(SQLALCHEMY_DATABASE_URI)

def generate_embedding(text):
    response = openai.Embedding.create(
        input=text,
        model="text-embedding-ada-002"
    )
    return response["data"][0]["embedding"]

def get_closest_questions(embedding, num_questions=20):
    # Convert the embedding from a list of floats to a list of strings
    embedding_str = [str(e) for e in embedding]

    # Join the embedding list into a single string, separated by commas
    embedding_str = ",".join(embedding_str)

    # Form the SQL query
    sql = text(f"""
    SELECT question
    FROM faq
    ORDER BY faq.question_embedding <-> array[{embedding_str}]::float[]
    LIMIT :num_questions
    """)

    # Execute the query
    result = engine.execute(sql, num_questions=num_questions)

    # Fetch the results and return the questions
    return [row['question'] for row in result]

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/get')
def get_bot_response():
    userText = request.args.get('msg')
    if userText is None or userText.strip() == '':
        abort(400, "msg parameter is required.")
    embedding = generate_embedding(userText)
    response = get_closest_questions(embedding)
    return jsonify({'questions': response, 'ids': [faq.id for faq in response]})

@app.route('/get_answer')
def get_answer():
    id = request.args.get('id')
    if id is None or id.strip() == '':
        abort(400, "id parameter is required.")
    faq = FAQ.query.get(id)
    if faq:
        return jsonify({'answer': faq.answer})
    else:
        return jsonify({'answer': "すいません。データが見つかりません。"})

from datetime import datetime

@app.route('/faq/new', methods=['GET', 'POST'])
def new_faq():
    if request.method == 'POST':
        question = request.form['question']
        answer = request.form['answer']
        question_embedding = generate_embedding(question)
        question_length = len(question)
        question_tokens = len(question.split())
        enable_flag = int(request.form['enable_flag']) if request.form['enable_flag'] else 0
        created_at = request.form['created_at'] if request.form['created_at'] else datetime.now()
        updated_at = request.form['updated_at'] if request.form['updated_at'] else datetime.now()

        new_faq = FAQ(
            question=question, 
            answer=answer, 
            question_embedding=question_embedding,
            question_length=question_length, 
            question_tokens=question_tokens, 
            enable_flag=enable_flag, 
            created_at=created_at, 
            updated_at=updated_at
        )
        db.session.add(new_faq)
        db.session.commit()

        return render_template('new_faq.html')

    return render_template('new_faq.html')


def search_faq(input_word):
    results = FAQ.query.filter(FAQ.question.ilike('%' + input_word + '%')).all()
    if results:
        return results
    else:
        return []

if __name__ == "__main__":
    app.run(debug=True)
