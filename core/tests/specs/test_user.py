import pytest
import json
from core.tests.fixtures import user_bob


# ---- Test création d'utilisateur ----

@pytest.mark.django_db
def test_create_user(client):
    # ---- Payload pour création ----
    user_payload = {
        "name": "Bob",
        "email": "bob@example.com",
        "password": "I_am_Bob",
    }

    # ---- Appel API POST pour créer un user ----
    response = client.post(
        "/core/user/create/",
        data=json.dumps(user_payload),
        content_type="application/json",
    )
    
    # ---- Vérification du statut ----
    assert response.status_code == 201
    created_user = response.json()
    
    # ---- Vérification des données retournées ----
    assert created_user["username"] == "Bob"
    assert created_user["email"] == "bob@example.com"
    assert created_user["id"] is not None
    
    # ---- Vérification que l'utilisateur est bien en base ----
    response = client.get(
        f"/core/user/get/?id={created_user['id']}",
    )
    assert response.status_code == 200
    assert response.json() == {
        "id": created_user["id"],
        "username": "Bob",
        "email": "bob@example.com",
    }

# ---- Test récupération du profil connecté (authentifié) ----
@pytest.mark.django_db
def test_get_my_profile__authenticated(client, user_bob):
    # ---- Connexion de l'utilisateur
    client.force_login(user_bob.user)

    # ---- Appel API GET pour récupérer profil
    response = client.get("/core/user/my_profile/")

    # ---- Vérifications
    assert response.status_code == 200
    assert response.json()["id"] == user_bob.id

# ---------------------------------------------------
# Test récupération du profil non authentifié
# ---------------------------------------------------
@pytest.mark.django_db
def test_get_my_profile__unauthenticated(client):
    # ---- Appel API GET sans connexion
    response = client.get("/core/user/my_profile/")

    # ---- Vérification : interdit
    assert response.status_code == 403