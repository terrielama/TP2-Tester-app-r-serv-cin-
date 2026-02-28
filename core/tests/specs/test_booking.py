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
def test_book_movie(mock_book_seat, user_bob):
    client = Client()
    client.force_login(user_bob.user)

    theater = Theater.objects.create(name="MK2 Gambetta", address="Paris", owner=user_bob)
    showtime = Showtime.objects.create(
        theater=theater,
        movie_name="Big Fight!",
        start_time=make_aware(datetime.datetime(2026, 12, 31, 22, 0, 0)),
        provider="MK2"
    )

    mock_book_seat.return_value = {"success": True}

    response = client.post(
        "/core/book_movie/",
        data=json.dumps({"showtime_id": showtime.id}),
        content_type="application/json"
    )

    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    # assert data["provider"] == "MK2"

    # ---- Vérification du mock avec datetime objet directement
    mock_book_seat.assert_called_once_with(
        theater_name="MK2 Gambetta",
        movie_name="Big Fight!",
        date=ANY
    )