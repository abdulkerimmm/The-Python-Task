from flask import Flask, render_template, request, redirect, url_for, session
from models import db, Question

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///quiz.db'
app.config['SECRET_KEY'] = 'your_secret_key'
db.init_app(app)

@app.route('/')
def home():
    questions = Question.query.all()
    return render_template('index.html', questions=questions)

@app.route('/submit', methods=['POST'])
def submit():
    score = 0
    total_questions = Question.query.count()
    for question in Question.query.all():
        user_answer = request.form.get(str(question.id))
        if user_answer == question.correct_answer:
            score += 1
    session['score'] = score
    if 'highest_score' not in session or score > session['highest_score']:
        session['highest_score'] = score
    return redirect(url_for('result'))

@app.route('/result')
def result():
    return render_template('result.html', score=session.get('score'), highest_score=session.get('highest_score'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
