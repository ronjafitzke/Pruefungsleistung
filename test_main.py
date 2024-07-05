# -*- coding: utf-8 -*-
from main import app
import unittest
import pytest

# -*- coding: utf-8 -*-
import pytest
from main import app


@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


def test_calculate_price_valid_input(client):
    rv = client.post('/calculator', data={'price1': '10', 'price2': '20'})
    assert b'30.0' in rv.data
    assert rv.status_code == 200


def test_calculate_price_invalid_input(client):
    rv = client.post('/calculator', data={'price1': 'abc', 'price2': '20'})
    assert b'Invalid input' in rv.data
    assert rv.status_code == 200


def test_calculate_dose_valid_input(client):
    rv = client.post('/dose', data={'einzeldosis': '5', 'häufigkeit': '3', 'zeitraum': '7'})
    assert b'17.142857' in rv.data
    assert rv.status_code == 200


def test_calculate_dose_invalid_input(client):
    rv = client.post('/dose', data={'einzeldosis': '5', 'häufigkeit': 'abc', 'zeitraum': '7'})
    assert b'Invalid input' in rv.data
    assert rv.status_code == 200


def test_calculate_BMI_valid_input(client):
    rv = client.post('/BMI', data={'height': '1.75', 'weight': '70'})
    assert b'22.857142' in rv.data
    assert rv.status_code == 200


def test_calculate_BMI_invalid_input(client):
    rv = client.post('/BMI', data={'height': 'abc', 'weight': '70'})
    assert b'Invalid input' in rv.data
    assert rv.status_code == 200

