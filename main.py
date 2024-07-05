# -*- coding: utf-8 -*-
from flask import Flask, render_template, request, flash, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)   # Erstellt die Flask Anwendung
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db' # Gibt den Pfad zur SQLite-Datenbankdatei an
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False    # Deaktiviert die SQLAlchemy Änderungsverfolgung, um Ressourcen zu sparen
app.config['SECRET_KEY'] = 'your_secret_key'    # geheimer Schlüssel, der für die Sitzungen und die Flash-Nachrichten verwendet wird
database = SQLAlchemy(app)  # erstellt eine SQLALchemy Instanz


class Users(database.Model):    # Datenbankmodell für die Benutzer
    id = database.Column(database.Integer, primary_key=True)
    email = database.Column(database.String(200), unique=True, nullable=False)
    password = database.Column(database.String(200), nullable=False)


class Medikament(database.Model):   # Datenbankmodell für die persönlichen Medikamente
    id = database.Column(database.Integer, primary_key=True)
    name = database.Column(database.String(200), nullable=False)
    dosierung = database.Column(database.String(200), nullable=False)
    hersteller = database.Column(database.String(200), nullable=False)
    time = database.Column(database.String(200), nullable=False)
    user_id = database.Column(database.Integer, database.ForeignKey('users.id'), nullable=False)
    user = database.relationship('Users', backref=database.backref('medikamente', lazy=True))


class Medizin(database.Model):  # Datenbankmodell für die allgemein verfügbaren Medikamente
    id = database.Column(database.Integer, primary_key=True)
    name = database.Column(database.String(200), nullable=False)
    hersteller = database.Column(database.String(200), nullable=False)
    anwendung = database.Column(database.String(500), nullable=False)
    rezeptpflichtig = database.Column(database.String(200), nullable=False)
    preis = database.Column(database.String(200), nullable=False)


# Datenbanktabellen erstellen
with app.app_context():
    database.create_all()   # erstellt alle Tabellen, die durch die Datenbankmodelle definiert sind

    if not Medizin.query.filter_by(name="Arcasin® TS").first(): # wenn die Tabelle leer ist:
        # Beispieldaten hinzufügen
        example_data = [
            Medizin(name="Arcasin® TS", hersteller="MEDA Pharma GmbH & Co. KG", anwendung="Leichte bis mittelschwere Infekt. mit Phenoxymethylpenicillin-sensiblen Erregern, wie z. B.: Infekt. des HNO-Bereiches, Infekt. der tiefen Atemwege, Infekt. im Zahn-, Mund- u. Kieferbereich, Endokarditisprophylaxe bei Eingriffen im Zahn-, Mund- u. Kieferbereich od. am oberen Respirationstrakt, Infekt. der Haut, Lymphadenitis, Lymphangitis, Infekt. durch β-häm. Streptokokken der Gruppe A, z. B. Scharlach, Erysipel, Rezidivprophylaxe bei rheumat. Fieber. Ggf. ist eine Komb. mit einem weiteren geeigneten Antibiotikum mögl.", rezeptpflichtig="Ja", preis="12,79€"),
            Medizin(name="Amoxi-saar® plus", hersteller="MIP Pharma GmbH", anwendung="Akute bakterielle Sinusitis (nach adäquater Diagnosestellung); akute Otitis media; akute Exazerbationen einer chronischen Bronchitis (nach adäquater Diagnosestellung); ambulant erworbene Pneumonie; Urozystitis; Pyelonephritis; Haut- und Weichteilinfektionen, insbesondere Infektionen der unteren Hautschichten, Tierbisse, schwere dentale Abszesse mit sich lokal ausbreitender Infektion; Knochen- und Gelenkinfektionen, insbesondere Osteomyelitis.", rezeptpflichtig="Ja", preis="2,58€"),
            Medizin(name="ARIKAYCE® liposomal", hersteller="Insmed Netherlands B.V.", anwendung="ARIKAYCE liposomal wird angewendet zur Behandlung von Lungeninfektionen, verursacht durch zum Mycobacterium-avium-Komplex (MAC) gehörende nicht-tuberkulöse Mykobakterien (NTM), bei Erwachsenen mit begrenzten Behandlungsoptionen, die keine zystische Fibrose haben.", rezeptpflichtig="Ja", preis="28,95€"),
            Medizin(name="Avalox", hersteller="Bayer Vital GmbH", anwendung="Behandl. v. folg. bakt. Infekt. bei Pat. ab 18 J. soweit durch Moxifloxacin-empfindl. Erreger hervorgerufen. In folg. Anw. sollte Moxifloxacin nur angew. werden, wenn and., üblicherw. für d. Behandl. empfohl. Antibiotika für ungeeignet erachtet werden: akute, bakt. Sinusitis; akute Exazerbat. e. chron. obstruktiven Lungenerkr. einschl. Bronchitis. In folg. Anw. sollte Moxifloxacin nur angew. werden, wenn and., üblicherw. f. d. initiale Behandl. empfohl. Antibiotika für ungeeignet erachtet werden od. versagt haben: ambulant erworb. Pneumonie, ausgen. schwere Formen; leichte bis mäßig schwere entzündl. Erkrank. des Beckens (d. h. Infekt. des oberen weibl. Genitaltrakts, einschl. Salpingitis u. Endometritis), ohne assoz. Tuboovarial- od. Beckenabszess. Nicht für eine Monother. v. leicht bis mäßig schweren entzündl. Erkrank. des Beckens empf., sondern aufgr. steig. Resistenz v. Neisseria gonorrhoeae in Komb. m. weit. geeign. Antibiotikum (z. B. Cephalosporin) zu geben, es sei denn, Moxifloxacin-resistente Neisseria gonorrhoeae können ausgeschl. werden. Abschließ. Behandl. b. Pat., die unter d. Initialther. m. i.v. Moxifloxacin in d. folg. Anw. eine Besser. gezeigt haben: ambulant erworb. Pneumonie, komplizierte Haut- u. Weichgewebeinfekt. Nicht z. Initialther. v. Haut- u. Weichgewebeinfekt. od. schwerer, ambulant erworb. Pneumonie anwenden.",rezeptpflichtig="Ja", preis="9,04€")
        ]

        for med in example_data:
            database.session.add(med)   # Jede Instanz von Medizin wird der aktuellen Sitzung hinzugefügt
        database.session.commit()


# Routen
@app.route("/")
def home():
    return render_template('home.html')


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST": # überprüft ob die Anfragemethode "Post" ist, alo ob das Registrierungsformular abgeschickt wurde
        email = request.form.get("email")
        password = request.form.get("password")
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')

        new_user = Users(email=email, password=hashed_password) # erstellt eine neue Instanz des User Modells
        database.session.add(new_user) # fügt die Daten in die Datenbank hinzu
        database.session.commit()
        flash("Registrierung erfolgreich! Sie können sich jetzt einloggen.")
        return redirect(url_for("login"))

    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        user = Users.query.filter_by(email=email).first() # Abfrage sucht nach einem Benutzer in der Datenbank, dessen E-Mail-Adresse mit der eingegebenen übereinstimmt
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
    session.pop('logged_in', None) # Entfernt die Session-Variable 'logged_in', die anzeigt, dass ein Benutzer eingeloggt ist
    return redirect(url_for('home'))


@app.route("/profile")
def profile():
    if not session.get("logged_in"):
        return redirect(url_for("login"))

    user_id = session.get("user_id")
    medications = Medikament.query.filter_by(user_id=user_id).all()
    return render_template("profile.html", medications=medications)


@app.route("/medikamente", methods=["GET", "POST"])
def medikamente():
    suche = request.args.get("suche")
    if suche:
        medikamente = Medizin.query.filter(Medizin.name.like(f"%{suche}%")).all()
    else:
        medikamente = Medizin.query.all()

    return render_template("medications.html", medikamente=medikamente)


@app.route("/add_my_medication", methods=["POST"])
def add_my_medication():
    if not session.get("logged_in"):
        return redirect(url_for("login"))

    name = request.form.get("name")
    dosierung = request.form.get("dosierung")
    hersteller = request.form.get("hersteller")
    time = request.form.get("time")
    user_id = session.get("user_id")

    new_medication = Medikament(name=name, dosierung=dosierung, hersteller=hersteller, time=time, user_id=user_id)
    database.session.add(new_medication)
    database.session.commit()

    flash("Medikament erfolgreich hinzugefügt!")
    return redirect(url_for("profile"))


@app.route("/calculator", methods=["GET", "POST"])
def calculate_price():
    result = None
    if request.method == "POST":
        try:
            price1 = float(request.form["price1"])
            price2 = float(request.form["price2"])
            result = price1 + price2
        except ValueError:
            result = "Invalid input. Please enter numeric values."
    return render_template("calculate_price.html", result=result)


@app.route("/dose", methods=["Get","Post"])
def calculate_dose():
    total_dose_per_day = None
    total_dose = None
    if request.method == "POST":
        try:
            single_dose = float(request.form["einzeldosis"])
            frequency = float(request.form["häufigkeit"])
            period = float(request.form["zeitraum"])
            doses_per_day = 24/frequency
            total_dose_per_day = single_dose * doses_per_day
            total_dose = total_dose_per_day * period
        except ValueError:
            total_dose_per_day = "Invalid input. Please enter numeric values."
            total_dose = "Invalid input. Please enter numeric values."
    return render_template("calculate_dose.html", total_dose_per_day=total_dose_per_day, total_dose=total_dose)


@app.route("/BMI", methods=["GET","POST"])
def calculate_BMI():
    bmi = None
    if request.method == "POST":
        try:
            height = float(request.form["height"])
            weight = float(request.form["weight"])
            bmi = weight/(height**2)
        except ValueError:
            bmi = "Invalid input. Please enter numeric values."
    return render_template("calculate_bmi.html", bmi=bmi)


if __name__ == "__main__":
    app.run(debug=True)
