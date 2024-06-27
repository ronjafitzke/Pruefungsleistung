# -*- coding: utf-8 -*-
import requests
from flask import Flask, render_template, request, flash, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'your_secret_key'  # Notwendig für Flash-Messages
database = SQLAlchemy(app)

# API URL
# Neue API URL und Header
url = "https://drugapi.p.rapidapi.com/Drug/Summary/Acetaminophen-and-Codeine-Phosphate-Oral-Solution-acetaminophen-codeine-phosphate-665"

headers = {
    "x-rapidapi-key": "a6261f39ffmsh6d2b2c8f6353733p12512cjsn13b0c4ace526",
    "x-rapidapi-host": "drugapi.p.rapidapi.com"
}

# Daten abrufen
response = requests.get(url, headers=headers)
data = response.json()


class Users(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    email = database.Column(database.String(200), unique=True, nullable=False)
    password = database.Column(database.String(200), nullable=False)


class Medikament(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    name = database.Column(database.String(200), nullable=False)
    hersteller = database.Column(database.String(200), nullable=False)
    dosierung = database.Column(database.String(200), nullable=False)
    beschreibung = database.Column(database.String(500), nullable=True)


# Datenbanktabellen erstellen
with app.app_context():
    database.create_all()

# Daten in die Datenbank einfügen
with app.app_context():
    # Extrahiere relevante Felder mit Fallback auf 'N/A', falls Felder nicht vorhanden sind
    name = data.get('name', 'N/A')
    hersteller = data.get('manufacturer', 'N/A')
    dosierung = data.get('dosage', 'N/A')
    beschreibung = data.get('description', 'N/A')

    # Medikament-Objekt erstellen
    new_medikament = Medikament(name=name, hersteller=hersteller, dosierung=dosierung, beschreibung=beschreibung)
    database.session.add(new_medikament)

    # Änderungen speichern
    database.session.commit()

print("Daten erfolgreich eingefügt.")


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

    return render_template("profile.html")


@app.route("/medikamente")
def medikamente():
    medikamente = Medikament.query.all()
    return render_template("medications.html", medikamente=medikamente)


if __name__ == "__main__":
    app.run(debug=True)
