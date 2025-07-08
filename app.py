from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, date, time


app = Flask(__name__)
app.secret_key = "your_secret_key"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///students.db"
db = SQLAlchemy(app)

# Simulated user database
users = {
    "Aravinth": {"password": "amma143", "role": "admin"},
    "teacher": {"password": "teacher123", "role": "teacher"},
    "magesh":{"password":"magesh","role":"admin "},
}

class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    roll_no = db.Column(db.Integer, unique=True, nullable=False)
    marks1 = db.Column(db.Integer, nullable=False)
    marks2 = db.Column(db.Integer, nullable=False)
    marks3 = db.Column(db.Integer, nullable=False)
    marks4 = db.Column(db.Integer, nullable=False)
    marks5 = db.Column(db.Integer, nullable=False)
    marks6 = db.Column(db.Integer, nullable=False)


    @property
    def average(self):
        return round((self.marks1 + self.marks2 + self.marks3 + self.marks4 + self.marks5 + self.marks6) / 6, 2)

    @property
    def grade(self):
        avg = self.average
        if avg >= 90: return "A"
        elif avg >= 80: return "B"
        elif avg >= 70: return "C"
        elif avg >= 60: return "D"
        else: return "F"

@app.route('/')
def index():
    if "user" not in session:
        return redirect(url_for("login"))

    return render_template('index.html', students=Student.query.all(), current_user=session["user"])

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form["username"]
        password = request.form["password"]

        if username in users and users[username]["password"] == password:
            session["user"] = {"username": username, "role": users[username]["role"]}
            return redirect(url_for("index"))
        else:
            return "invalid credentials"

    return render_template("login.html")

@app.route('/logout')
def logout():
    session.pop("user", None)  # Remove user from session
    return redirect(url_for("login"))

@app.route('/add_student', methods=['POST'])
def add_student():
    if "user" not in session or session["user"]["role"] not in ["admin", "teacher"]:
        return redirect(url_for("index"))

    student = Student(
        name=request.form["name"],
        roll_no=request.form["roll_no"],
        marks1=request.form["marks1"],
        marks2=request.form["marks2"],
        marks3=request.form["marks3"],
        marks4=request.form["marks4"],
        marks5=request.form["marks5"],
        marks6=request.form["marks6"],
    )
    db.session.add(student)
    db.session.commit()
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    return redirect(url_for("index"))

@app.route('/update_student/<int:id>', methods=['GET', 'POST'])
def update_student(id):
    student = Student.query.get_or_404(id)
    if request.method == 'POST':
        student.name = request.form['name']
        student.roll_no = request.form['roll_no']
        student.marks1 = request.form['marks1']
        student.marks2 = request.form['marks2']
        student.marks3 = request.form['marks3']
        student.marks4 = request.form['marks4']
        student.marks5 = request.form['marks5']
        student.marks6 = request.form['marks6']
        db.session.commit()
        updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow)
        return redirect(url_for('index'))
    return render_template('update.html', student=student)


@app.route('/delete_student/<int:id>')
def delete_student(id):
    if "user" not in session or session["user"]["role"] != "admin":
        return redirect(url_for("index"))

    student = Student.query.get(id)
    db.session.delete(student)
    db.session.commit()
    return redirect(url_for("index"))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
