import pytest
import json
import datetime
from django.test import Client
from django.utils.timezone import make_aware
from unittest.mock import patch
from django.contrib.auth.models import User
from core.models import BookUser, Theater, Showtime
from unittest.mock import ANY


# ---- Fixture utilisateur ----
@pytest.fixture
def user_bob(db):
    user = User.objects.create_user(username="Bob", email="bob@example.com", password="I_am_Bob")
    return BookUser.objects.create(user=user, is_company=False)

@pytest.mark.django_db
@patch("external_apis.mk2.book_seat")
@patch("external_apis.ugc.book_seat")
@patch("external_apis.gaumont.book_seat")
def test_book_showtime(mock_gaumont, mock_ugc, mock_mk2, user_bob):
    client = Client()
    client.force_login(user_bob.user)

    # ---- Création des théâtres et séances
    theater_mk2 = Theater.objects.create(name="MK2 Gambetta", address="Paris", owner=user_bob)
    theater_ugc = Theater.objects.create(name="UGC Opéra", address="Paris", owner=user_bob)
    theater_gaumont = Theater.objects.create(name="Gaumont Champs", address="Paris", owner=user_bob)

    show_mk2 = Showtime.objects.create(
        theater=theater_mk2,
        movie_name="Big Fight!",
        start_time=make_aware(datetime.datetime(2026, 12, 31, 22, 0, 0)),
        provider="MK2"
    )
    show_ugc = Showtime.objects.create(
        theater=theater_ugc,
        movie_name="Comedy Night",
        start_time=make_aware(datetime.datetime(2026, 12, 30, 20, 0, 0)),
        provider="UGC"
    )
    show_gaumont = Showtime.objects.create(
        theater=theater_gaumont,
        movie_name="Action Movie",
        start_time=make_aware(datetime.datetime(2026, 12, 29, 18, 0, 0)),
        provider="Gaumont"
    )

    # ---- Retours des mocks
    mock_mk2.return_value = {"success": True, "provider": "MK2"}
    mock_ugc.return_value = {"success": True, "provider": "UGC"}
    mock_gaumont.return_value = {"success": True, "provider": "Gaumont"}

    # ---- Réserver chaque séance
    for showtime in [show_mk2, show_ugc, show_gaumont]:
        response = client.post(
            "/core/book_movie/",
            data=json.dumps({"showtime_id": showtime.id}),
            content_type="application/json"
        )
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert data["provider"] == showtime.provider

    # ---- Vérification du mock MK2
    mock_mk2.assert_called_once_with(
        theater_name="MK2 Gambetta",
        movie_name="Big Fight!",
        date=ANY
    )