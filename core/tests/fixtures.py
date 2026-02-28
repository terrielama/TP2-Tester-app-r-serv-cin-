import pytest
from django.contrib.auth.models import User
from core.models import BookUser


# ---- Fixture : utilisateur classique ----
@pytest.fixture
def user_bob(db):
    # ---- Création du User Django (authentification) ----
    user = User.objects.create_user(
        username="Bob",
        email="bob@example.com",
        password="I_am_Bob",
    )

    # ---- Création du profil métier BookUser ----
    book_user = BookUser.objects.create(
        user=user,
        is_company=False,  # ---- Utilisateur simple ----
    )

    return book_user


# ----------- Fixture : utilisateur propriétaire (Company) ----

@pytest.fixture
def user_company(db):
    # ---- Création du User Django ----
    user = User.objects.create_user(
        username="CinemaOwner",
        email="owner@example.com",
        password="secure_password",
    )

    # ---- Création du BookUser avec rôle propriétaire ----
    book_user = BookUser.objects.create(
        user=user,
        is_company=True,  # ---- Indique qu'il peut créer des salles ----
    )

    return book_user