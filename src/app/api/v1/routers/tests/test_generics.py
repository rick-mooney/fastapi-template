import random
import pytest
import json
from app.api.schemas import (
    UserOut
)

from app.db.models import (User)

def test_unauthenticated_routes(client):
    response = client.get("/api/v1/user/1")
    assert response.status_code == 401

def test_admin_list_user(client, superuser_token_headers):
    response = client.get("/api/v1/user", headers=superuser_token_headers)
    assert response.status_code == 200
    data = response.json()
    print(data)
    assert data['total'] == 1

def test_user_list_unauthenticated(client, user_token_headers):
    response = client.get("/api/v1/user", headers=user_token_headers)
    assert response.status_code == 200
    data = response.json()
    assert data['total'] == 0

def test_user_create(client, superuser_token_headers):  
    user_info = {"email": "test@test.com", "first_name": "Test First Name", "last_name": "Test Last Name" }
    response = client.post("/api/v1/user", headers=superuser_token_headers, json=(user_info))
    assert response.status_code == 200

def test_get_record(client, superuser_token_headers, db_connection):
    user = db_connection.query(User).filter(User.email == 'test@test.com').first()
    response = client.get(f"/api/v1/user/{user.external_id}", headers=superuser_token_headers)
    assert response.status_code == 200

def test_user_update(client, superuser_token_headers, db_connection):
    user = db_connection.query(User).filter(User.email == 'test@test.com').first()
    data = {"first_name": "changed"}
    response = client.put(f"/api/v1/user/{user.external_id}", headers=superuser_token_headers, json=data)
    assert response.status_code == 200

def test_user_delete(client, superuser_token_headers, db_connection):
    user = db_connection.query(User).filter(User.email == 'test@test.com').first()
    response = client.delete(f"/api/v1/user/{user.external_id}", headers=superuser_token_headers)
    assert response.status_code == 200