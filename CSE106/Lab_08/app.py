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



# class User(db.Model, UserMixin):
#     id = db.Column(db.Integer, primary_key=True)
#     username = db.Column(db.String(20), nullable=False)
#     password = db.Column(db.String(80), nullable=False)

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password_hash = db.Column(db.String(120))
    role = db.Column(db.String(10))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

def create_admin_user():
    admin_username = 'admin'
    admin_password = 'admin123'  # You should move this to a configuration file or environment variable.

    existing_admin = User.query.filter_by(username=admin_username).first()
    if not existing_admin:
        admin_user = User(
            username=admin_username,
            role='admin'
        )
        admin_user.set_password(admin_password)
        db.session.add(admin_user)
        db.session.commit()
        print("Admin user created")
    else:
        # to not reset the password every time, comment the following lines.
        existing_admin.set_password(admin_password)
        db.session.commit()
        print("Admin user already exists")


with app.app_context():
    db.create_all()
    create_admin_user()



# users = {
#     'john_student': User('1', 'john_student', generate_password_hash('password'), 'student'),
#     'jane_teacher': User('2', 'jane_teacher', generate_password_hash('password'), 'teacher'),
#     # Add more users as needed
# }

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        #print(user)
        
        if user and user.check_password(password):
            #print("debug check")
            login_user(user)
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
#@login_required
def myStudentCourses():
    return render_template('myStudentCourses.html')

@app.route('/teacherCourses')
#@login_required
def teacherCourses():
    return render_template('teacherCourses.html')

@app.route('/logout')
#@login_required
def logout():
    logout_user()
    return 'Logged out'


@app.route('/admin/add_user', methods=['POST'])
def add_user():
    username = request.form['username']
    password = request.form['password']
    role = request.form['role']

    user = User(username=username, role=role)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()
    return redirect(url_for('adminData'))

@app.route('/admin/edit_user/<int:user_id>', methods=['POST'])
def edit_user(user_id):
    user = User.query.get(user_id)
    user.username = request.form['username']
    user.set_password(request.form['password'])
    user.role = request.form['role']
    db.session.commit()
    return redirect(url_for('adminData'))

@app.route('/admin/delete_user/<int:user_id>', methods=['POST'])
def delete_user(user_id):
    user = User.query.get(user_id)
    db.session.delete(user)
    db.session.commit()
    return redirect(url_for('adminData'))

@app.route('/admin')
def adminData():
    users = User.query.all()
    return render_template('adminData.html', users=users)



if __name__ == '__main__':
    app.run(debug=True)
