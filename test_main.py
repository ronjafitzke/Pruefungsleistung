# -*- coding: utf-8 -*-
import pytest
from main import app


@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


def test_calculate_price_valid_input(client):
    response_value = client.post('/calculator', data={'price1': '10', 'price2': '20'})   # Antwortdaten liegen im Bytes Format vor
    response_data = response_value.data.decode('utf-8') # umwandeln in UTF-8 codierten String
    assert "30.0" in response_data
    assert response_value.status_code == 200


def test_calculate_price_invalid_input(client):
    response_value = client.post('/calculator', data={'price1': 'abc', 'price2': '20'})
    response_data = response_value.data.decode('utf-8')
    assert "Invalid input" in response_data
    assert response_value.status_code == 200


def test_calculate_dose_valid_input(client):
    response_value = client.post('/dose', data={'einzeldosis': '5', 'häufigkeit': '4', 'zeitraum': '7'})
    response_data = response_value.data.decode('utf-8')
    assert "Gesamtdosis pro Tag: 30.0 mg" in response_data
    assert "Gesamtdosis: 210.0 mg" in response_data
    assert response_value.status_code == 200


def test_calculate_dose_invalid_input(client):
    response_value = client.post('/dose', data={'einzeldosis': '5', 'häufigkeit': 'abc', 'zeitraum': '7'})
    response_data = response_value.data.decode('utf-8')
    assert "Invalid input" in response_data
    assert response_value.status_code == 200


def test_calculate_BMI_valid_input(client):
    response_value = client.post('/BMI', data={'height': '1.75', 'weight': '70'})
    response_data = response_value.data.decode('utf-8')
    assert "22.857142" in response_data
    assert response_value.status_code == 200


def test_calculate_BMI_invalid_input(client):
    response_value = client.post('/BMI', data={'height': 'abc', 'weight': '70'})
    response_data = response_value.data.decode('utf-8')
    assert "Invalid input" in response_data
    assert response_value.status_code == 200

