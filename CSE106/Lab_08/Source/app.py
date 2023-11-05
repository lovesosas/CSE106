from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('\Users\Luis\Documents\Code\CSE106\Lab_08\HTML\index.html')

@app.route('/myStudentCourses')
def about():
    return render_template('\Users\Luis\Documents\Code\CSE106\Lab_08\HTML\student\myStudentCourses.html')

if __name__ == '__main__':
    app.run(debug=True)
