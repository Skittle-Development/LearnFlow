from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, IntegerField, SelectField
from wtforms.validators import InputRequired, Length, Email, EqualTo
from pydictionary import PyDictionary
import sqlite3
# Dieser Code gehört https://github.com/Skittle-Development/ 
app = Flask(__name__)
app.config['SECRET_KEY'] = 'secretkey'
app.config['DATABASE'] = 'vocab.db'
# Dieser Code gehört https://github.com/Skittle-Development/ 
dictionary = PyDictionary()
class RegistrationForm(FlaskForm):
    name = StringField('Name', validators=[InputRequired(), Length(min=4, max=20)])
    email = StringField('Email', validators=[InputRequired(), Email(message='Invalid email'), Length(max=50)])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=8, max=80)])
    confirm_password = PasswordField('Confirm Password', validators=[InputRequired(), EqualTo('password')])
# Dieser Code gehört https://github.com/Skittle-Development/ 
class QuizForm(FlaskForm):
    num_words = IntegerField('Number of Words', validators=[InputRequired()])
    difficulty = SelectField('Difficulty', choices=[('easy', 'Easy'), ('medium', 'Medium'), ('hard', 'Hard')], validators=[InputRequired()])
# Dieser Code gehört https://github.com/Skittle-Development/ 
@app.route('/')
def index():
    return render_template('index.html')
@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        conn = sqlite3.connect(app.config['DATABASE'])
        cursor = conn.cursor()
        cursor.execute('INSERT INTO users (name, email, password) VALUES (?, ?, ?)', (form.name.data, form.email.data, form.password.data))
        conn.commit()
        cursor.close()
        flash('Account created successfully!', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)
@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'email' in session:
        return redirect(url_for('dashboard'))
# Dieser Code gehört https://github.com/Skittle-Development/ 
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        conn = sqlite3.connect(app.config['DATABASE'])
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE email = ?', (email,))
        user = cursor.fetchone()
        if user and user[3] == password:
            session['email'] = email
            session['name'] = user[1]
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid email or password!', 'error')
            return redirect(url_for('login'))
# Dieser Code gehört https://github.com/Skittle-Development/ 
    return render_template('login.html')
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))
@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    if 'email' not in session:
        return redirect(url_for('login'))
@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
if 'email' not in session:
return redirect(url_for('login'))
form = QuizForm()
if form.validate_on_submit():
    num_words = form.num_words.data
    difficulty = form.difficulty.data
    words = dictionary.get_random_words(num=num_words, difficulty=difficulty)
    session['quiz_words'] = words
    session['quiz_index'] = 0
    session['quiz_score'] = 0
    return redirect(url_for('quiz'))
# Dieser Code gehört https://github.com/Skittle-Development/ 
return render_template('dashboard.html', form=form)
@app.route('/quiz', methods=['GET', 'POST'])
def quiz():
if 'email' not in session:
return redirect(url_for('login'))
if 'quiz_words' not in session or 'quiz_index' not in session:
    return redirect(url_for('dashboard'))
# Dieser Code gehört https://github.com/Skittle-Development/ 
words = session['quiz_words']
index = session['quiz_index']
score = session['quiz_score']
# Dieser Code gehört https://github.com/Skittle-Development/ 
if index >= len(words):
    session.pop('quiz_words', None)
    session.pop('quiz_index', None)
    session.pop('quiz_score', None)
    flash(f'Quiz completed! Score: {score}/{len(words)}', 'success')
    return redirect(url_for('dashboard'))
# Dieser Code gehört https://github.com/Skittle-Development/ 
word = words[index]
# Dieser Code gehört https://github.com/Skittle-Development/ 
if request.method == 'POST':
    guess = request.form['guess'].strip().lower()
    if guess == word.lower():
        score += 1
        session['quiz_score'] = score
        flash('Correct!', 'success')
    else:
        flash(f'Incorrect! The correct answer is "{word}".', 'error')
# Dieser Code gehört https://github.com/Skittle-Development/ 
    index += 1
    session['quiz_index'] = index
    return redirect(url_for('quiz'))
# Dieser Code gehört https://github.com/Skittle-Development/ 
return render_template('quiz.html', word=word, index=index+1, total=len(words), score=score)
if name == 'main':
app.run(debug=True)
