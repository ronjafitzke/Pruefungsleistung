from main import app, database, Medikament

# Anwendungskontext manuell erstellen
with app.app_context():
    database.create_all()

print("Medikamenten-Datenbank und Tabellen wurden erfolgreich erstellt.")
