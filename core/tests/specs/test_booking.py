import pytest
import json
from unittest.mock import patch
from core.tests.fixtures import user_bob

# ---------------------------------------------------
# Test réservation d'une séance de cinéma
# ---------------------------------------------------
@pytest.mark.django_db
@patch("external_apis.mk2.book_seat")  # ---- Mock de l'API externe MK2
def test_book_movie(mock_book_seat, client, user_bob):
    # ---- Connexion de l'utilisateur
    client.force_login(user_bob.user)

    # ---- Payload de réservation
    payload = {
        "theater_id": 1,
        "movie_name": "Big Fight!",
        "date": "2026-12-31 22:00:00",
    }

    # ---- Simulation de la réponse de l'API externe
    mock_book_seat.return_value = {"success": True}

    expected_theater_name = "MK2 Gambetta"

    # ---- Appel API POST pour réserver la séance
    response = client.post(
        "/core/book_movie/",
        data=json.dumps(payload),
        content_type="application/json",
    )

    # ---- Vérification du statut HTTP
    assert response.status_code == 200

    # ---- Vérification que l'API externe a été appelée correctement
    mock_book_seat.assert_called_once_with(
        theater_name=expected_theater_name,
        movie_name="Big Fight!",
        date="2026-12-31 22:00:00",
    )