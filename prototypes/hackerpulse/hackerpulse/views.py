from hackerpulse import app
from flask import render_template

@app.route('/')
def index():
	return render_template('base.html')
	
@app.route('/login/')
def login():
	return "Login page goes here"
	
@app.route('/create/')
def create_account():
	return "form to enter feeds, etc"
	
@app.route('/<username>/')
def user_pulse(username):
	return render_template('user_pulse.html')