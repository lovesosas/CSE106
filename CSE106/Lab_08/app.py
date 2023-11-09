from flask import Flask, render_template, url_for #pip install flask
from flask_sqlalchemy import SQLAlchemy #pip install Flask-SQLAlchemy
from flask_login import UserMixin #pip install Flask-Login

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SECRET_KEY'] = 'key'
db = SQLAlchemy(app)

with app.app_context():
    # Now you can perform database operations, such as creating tables
    db.create_all()


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False)
    password = db.Column(db.String(80), nullable=False)


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/myStudentCourses')
def myStudentCourses():
    return render_template('myStudentCourses.html')

@app.route('/teacherCourses')
def teacherCourses():
    return render_template('teacherCourses.html')

if __name__ == '__main__':
    app.run(debug=True)
