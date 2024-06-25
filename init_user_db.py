from main import app, db

# Anwendungskontext manuell erstellen
with app.app_context():
    db.create_all()

print("Benutzer-Datenbank und Tabellen wurden erfolgreich erstellt.")
