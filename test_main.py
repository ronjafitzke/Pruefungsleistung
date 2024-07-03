# -*- coding: utf-8 -*-
from main import app, database, Users, Medikament, Medizin
import unittest
from werkzeug.security import generate_password_hash


# Funktionen zum Einrichten und Abreißen der Testumgebung
# konfiguriert den Flask-Testmodus, erstellt einen Testclient und richtet eine SQLite-In-Memory-Datenbank für Tests ein
def setUpModule():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///instance/database.db'
    global test_client  # test-client simuliert HTTP-Anfragen
    test_client = app.test_client()
    with app.app_context():
        database.create_all()


# räumt auf, indem die Session entfernt und die Testdatenbanktabellen gelöscht werden.
def tearDownModule():
    with app.app_context():
        database.session.remove()
        database.drop_all()


def test_register():
    with app.app_context():
        # Registrierung eines neuen Nutzers
        response = test_client.post('/register', data=dict(
            email='test@example.com',
            password='password123'
        ), follow_redirects=True)

        # Überprüfen, ob die Registrierung erfolgreich war
        assert response.status_code == 200
        assert 'Registrierung erfolgreich! Sie können sich jetzt einloggen.'.encode('utf-8') in response.data

        # Überprüfen, ob der Nutzer in der Datenbank gespeichert wurde
        user = Users.query.filter_by(email='test@example.com').first()
        assert user is not None


def test_login():
    with app.app_context():
        # Erstellung eines neuen Nutzers in der Datenbank
        hashed_password = generate_password_hash('password123', method='pbkdf2:sha256')
        user = Users(email='test@example.com', password=hashed_password)
        database.session.add(user)
        database.session.commit()

        # Login mit den erstellten Anmeldeinformationen
        response = test_client.post('/login', data=dict(
            email='test@example.com',
            password='password123'
        ), follow_redirects=True)

        # Überprüfen, ob der Login erfolgreich war
        assert response.status_code == 200
        assert "Login erfolgreich!"

        # Überprüfen, ob die Sitzung als eingeloggt markiert ist
        with test_client.session_transaction() as sess:
            assert sess['logged_in'] is True


def test_add_my_medication():
    with app.app_context():
        # Erstellung eines neuen Nutzers in der Datenbank
        hashed_password = generate_password_hash('password123', method='pbkdf2:sha256')
        user = Users(email='test@example.com', password=hashed_password)
        database.session.add(user)
        database.session.commit()

        # Manuelles Setzen der Sitzung als eingeloggt
        with test_client.session_transaction() as sess:
            sess['logged_in'] = True
            sess['user_id'] = user.id

        # Hinzufügen eines neuen Medikaments
        response = test_client.post('/add_my_medication', data=dict(
            name='TestMedikament',
            dosierung='20mg',
            hersteller='TestHersteller'
        ), follow_redirects=True)

        # Überprüfen, ob das Medikament erfolgreich hinzugefügt wurde
        assert response.status_code == 200
        assert "Medikament erfolgreich hinzugefügt!"

        # Überprüfen, ob das Medikament in der Datenbank gespeichert wurde
        medication = Medikament.query.filter_by(name='TestMedikament').first()
        assert medication is not None
        assert medication.dosierung == '20mg'
        assert medication.hersteller == 'TestHersteller'
        assert medication.user_id == user.id


if __name__ == '__main__':
    unittest.main()
