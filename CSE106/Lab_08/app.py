from flask import Flask, render_template, url_for, request, redirect #pip install flask
from flask_sqlalchemy import SQLAlchemy #pip install Flask-SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user #pip install Flask-Login
from werkzeug.security import generate_password_hash, check_password_hash
from flask_cors import CORS



app = Flask(__name__)
CORS(app)
app.secret_key = 'test123'

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SECRET_KEY'] = 'key'
db = SQLAlchemy(app)

with app.app_context():
    # Now you can perform database operations, such as creating tables
    db.create_all()


# class User(db.Model, UserMixin):
#     id = db.Column(db.Integer, primary_key=True)
#     username = db.Column(db.String(20), nullable=False)
#     password = db.Column(db.String(80), nullable=False)

class User(UserMixin):
    def __init__(self, id, username, password_hash, role):
        self.id = id
        self.username = username
        self.password_hash = password_hash
        self.role = role


users = {
    'john_student': User('1', 'john_student', generate_password_hash('password'), 'student'),
    'jane_teacher': User('2', 'jane_teacher', generate_password_hash('password'), 'teacher'),
    # Add more users as needed
}

@login_manager.user_loader
def load_user(user_id):
    for user in users.values():
        if user.id == user_id:
            return user
    return None

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = users.get(username)

        if user and check_password_hash(user.password_hash, password):
            if user.role == 'student':
                return redirect(url_for('myStudentCourses'))
            elif user.role == 'teacher':
                return redirect(url_for('teacherCourses'))
            elif user.role == 'admin':
                return redirect(url_for('adminData'))
            else:
                return redirect(url_for('index'))
        else:
            return 'Invalid username or password'

    return render_template('index.html')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/myStudentCourses')
@login_required
def myStudentCourses():
    return render_template('myStudentCourses.html')

@app.route('/teacherCourses')
@login_required
def teacherCourses():
    return render_template('teacherCourses.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return 'Logged out'

if __name__ == '__main__':
    app.run(debug=True)
