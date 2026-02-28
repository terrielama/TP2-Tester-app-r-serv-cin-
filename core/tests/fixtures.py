import pytest
import json
import datetime
from unittest.mock import patch
from django.test import Client
from django.utils.timezone import make_aware
from django.contrib.auth.models import User
from core.models import BookUser, Theater, Showtime

# ---- Fixture : utilisateur classique ----
@pytest.fixture
def user_bob(db):
    """
    Crée un utilisateur normal (non company) pour les tests.
    """
    user = User.objects.create_user(
        username="Bob",
        email="bob@example.com",
        password="I_am_Bob",
    )
    return BookUser.objects.create(user=user, is_company=False)


# ---- Fixture : utilisateur propriétaire (Company) ----
@pytest.fixture
def user_company(db):
    """
    Crée un utilisateur company (propriétaire de salle).
    """
    user = User.objects.create_user(
        username="CinemaOwner",
        email="owner@example.com",
        password="secure_password",
    )
    return BookUser.objects.create(user=user, is_company=True)


# ---- Fixture : Théâtre pour MK2 ----
@pytest.fixture
def theater_mk2(user_company):
    """
    Crée un théâtre appartenant à user_company pour les tests.
    """
    return Theater.objects.create(
        name="MK2 Gambetta",
        address="Paris",
        owner=user_company
    )


# ---- Fixture : Séance MK2 ----
@pytest.fixture
def showtime_mk2(theater_mk2):
    """
    Crée une séance pour le théâtre MK2 avec date aware pour timezone.
    """
    start_time = make_aware(datetime.datetime(2026, 12, 31, 22, 0, 0))
    return Showtime.objects.create(
        theater=theater_mk2,
        movie_name="Big Fight!",
        start_time=start_time,
        provider="MK2"
    )