from main import app, database, Users

# Anwendungskontext manuell erstellen
with app.app_context():
    database.create_all()

print("Benutzer-Datenbank und Tabellen wurden erfolgreich erstellt.")
