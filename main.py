# -*- coding: utf-8 -*-
from flask import Flask, render_template, request, flash, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'your_secret_key'  # Notwendig für Flash-Messages
database = SQLAlchemy(app)


class Users(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    email = database.Column(database.String(200), unique=True, nullable=False)
    password = database.Column(database.String(200), nullable=False)


class Medications(database.Model):
    name = database.Column(database.Integer, primary_key=True)
    amount = database.Column(database.String(200), nullable=False)
    date = database.Column(database.DateTime(), default=datetime.utcnow, nullable=False)


@app.route("/")
def home():
    return render_template('home.html')


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')

        new_user = Users(email=email, password=hashed_password)
        database.session.add(new_user)
        database.session.commit()
        flash("Registrierung erfolgreich! Sie können sich jetzt einloggen.")
        return redirect(url_for("login"))

    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        user = Users.query.filter_by(email=email).first()
        if user and check_password_hash(user.password, password):
            session["logged_in"] = True
            session["user_id"] = user.id
            flash("Login erfolgreich!")
            return redirect(url_for("start_page"))
        else:
            flash("Ungültige E-Mail oder Passwort")

    return render_template("login.html")


@app.route("/logout")
def logout():
    session.pop('logged_in', None)  # Lösche die Session-Variable für eingeloggten Benutzer
    return redirect(url_for('start_page'))


@app.route("/profile")
def profile():
    if not session.get("logged_in"):
        return redirect(url_for("login"))

    medications = Medications.query.all()
    return render_template("profile.html", medications=medications)


@app.route("/medications")
def medications():
    return render_template("medications.html")


if __name__ == "__main__":
    app.run(debug=True)