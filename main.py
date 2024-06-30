# -*- coding: utf-8 -*-
from flask import Flask, render_template, request, flash, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'your_secret_key'
database = SQLAlchemy(app)


class Users(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    email = database.Column(database.String(200), unique=True, nullable=False)
    password = database.Column(database.String(200), nullable=False)


class Medikament(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    name = database.Column(database.String(200), nullable=False)
    dosierung = database.Column(database.String(200), nullable=False)
    hersteller = database.Column(database.String(200), nullable=False)
    user_id = database.Column(database.Integer, database.ForeignKey('users.id'), nullable=False)
    user = database.relationship('Users', backref=database.backref('medikamente', lazy=True))


class Medikamente(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    name = database.Column(database.String(200), nullable=False)
    dosierung = database.Column(database.String(200), nullable=False)
    hersteller = database.Column(database.String(200), nullable=False)
    anwendung = database.Column(database.String(500), nullable=False)
    Verschreibungspflichtig = database.Column(database.String(200), nullable=False)


# Datenbanktabellen erstellen
with app.app_context():
    database.create_all()


# Restlicher Flask-Code bleibt unverändert
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
            return redirect(url_for("home"))
        else:
            flash("Ungültige E-Mail oder Passwort")

    return render_template("login.html")


@app.route("/logout")
def logout():
    session.pop('logged_in', None)  # Lösche die Session-Variable für eingeloggten Benutzer
    return redirect(url_for('home'))


@app.route("/profile")
def profile():
    if not session.get("logged_in"):
        return redirect(url_for("login"))

    user_id = session.get("user_id")
    medications = Medikament.query.filter_by(user_id=user_id).all()
    return render_template("profile.html", medications=medications)


@app.route("/medikamente")
def medikamente():
    medikamente = Medikament.query.all()
    return render_template("medications.html", medikamente=medikamente)


@app.route("/add_my_medication", methods=["POST"])
def add_my_medication():
    if not session.get("logged_in"):
        return redirect(url_for("login"))

    name = request.form.get("name")
    dosierung = request.form.get("dosierung")
    hersteller = request.form.get("hersteller")
    user_id = session.get("user_id")

    new_medication = Medikament(name=name, dosierung=dosierung, hersteller=hersteller, user_id=user_id)
    database.session.add(new_medication)
    database.session.commit()

    flash("Medikament erfolgreich hinzugefügt!")
    return redirect(url_for("profile"))


if __name__ == "__main__":
    app.run(debug=True)
