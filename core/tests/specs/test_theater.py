import pytest
import json
from core.tests.fixtures import user_company
from core.models import Theater 
@pytest.mark.django_db
def test_create_theater(client, user_company):
    # ---- Connexion du user company
    client.force_login(user_company.user)

    # ---- Payload pour la création de la salle
    payload = {
        "name": "MK2 Bastille",
        "address": "Paris",
    }

    # ---- Appel API POST pour créer la salle (avec slash final !)
    response = client.post(
        "/core/theater/create/",  # <--- slash ajouté
        data=json.dumps(payload),
        content_type="application/json",
    )

    # ---- Vérification du statut HTTP
    assert response.status_code == 201

    # ---- Vérification du contenu renvoyé par la vue
    data = response.json()
    assert data["name"] == "MK2 Bastille"
    assert data["address"] == "Paris"

    # ---- Vérification que l'objet Theater a bien été créé en base
    theater = Theater.objects.get(name="MK2 Bastille")
    assert theater.address == "Paris"
    assert theater.owner == user_company  # ---- Assure que le propriétaire est correct