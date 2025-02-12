from flask import Flask, render_template, flash, redirect, url_for, request, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:manish@localhost/karthik'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'your_secret_key_here'
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)

    
@app.route("/authors")
def authors():
    return render_template("authors.html")
@app.route("/books")
def books():
    return render_template("books.html")
@app.route("/contact")
def contact():
    return render_template("contact.html")
@app.route("/mainpage")
def mainpage():
    return render_template("mainpage.html")







@app.route("/")
def index():
    return render_template("index.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        print(request.form)  
        uname = request.form.get("uname") 
        passw = request.form.get("passw") 
        
        login_user = User.query.filter_by(username=uname, password=passw).first()
        
        if login_user:
            session["user_id"] = login_user.id
            session["username"] = login_user.username
            return redirect(url_for("mainpage"))
        else:
            flash("Invalid username or password!", "danger")
    return render_template("login.html")



@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        uname = request.form['uname']
        mail = request.form['mail']
        passw = request.form['passw']

        
        new_user = User(username=uname, email=mail, password=passw)
        db.session.add(new_user)
        db.session.commit()

       
        return redirect(url_for("login"))
    return render_template("register.html")

if __name__ == "__main__":
    with app.app_context():
        db.create_all()  
    app.run(debug=True)
