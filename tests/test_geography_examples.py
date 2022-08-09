"""Tests the Geography API"""
from pprint import pprint

from flask_jwt_extended import create_access_token
from app import db
from app.db.models import City, Country, User


def test_create_city_country(application):
    """This test creating the city and country"""
    with application.app_context():
        country = Country(name="United States")
        db.session.add(country)
        db.session.commit()
        city = City(name="New York", country_id=country.id)
        db.session.add(city)
        db.session.commit()

        assert city.country.name == "United States"


def test_country_post(client):
    """This tests country post"""
    with client.application.app_context():
        access_token = create_token()

    data = {"name": "United States"}

    headers = {
        'Authorization': 'Bearer {}'.format(access_token)  # pylint: disable=consider-using-f-string
    }
    response = client.post('/geography/countries', json=data, headers=headers)
    response_data = response.get_json()
    assert response.status_code == 201
    assert response_data["name"] == "United States"


def test_city__post(client):
    """This tests city post"""
    with client.application.app_context():
        access_token = create_token()

    data = {"name": "United States"}

    headers = {
        'Authorization': 'Bearer {}'.format(access_token)  # pylint: disable=consider-using-f-string
    }
    response = client.post('/geography/countries', json=data, headers=headers)
    response_data = response.get_json()
    country_id = response_data['id']
    pprint(country_id)

    data = {"country_id": country_id, "name": "Newark"}

    response = client.post('/geography/cities', json=data, headers=headers)
    assert response.status_code == 201
    response_data = response.get_json()
    assert response_data["id"] == 1
    assert response_data["name"] == "Newark"


def create_token():
    """Tests creating token"""
    user = User.query.first()
    access_token = create_access_token(user.access_token)
    return access_token
