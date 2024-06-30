# -*- coding: utf-8 -*-
from main import app, database

# Anwendungskontext manuell erstellen
with app.app_context():
    database.create_all()

print("Benutzer- und Medikamenten-Datenbank sowie Tabellen wurden erfolgreich erstellt.")
