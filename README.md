# TP2: Tester une application de réservation de cinéma

Groupe : Mathilde DELEKTA
		 Wallen JEAN MARIE ALPHONSINE
		 Terrie LAMA

-------------------------

 - Activer l'env :
  .venv\Scripts\activate

 - Installe les packages
uv sync

- Créer la base de données
uv run python manage.py makemigrations
uv run python manage.py migrate

- Run les test
uv run pytest

--------------------------

- Créer un système utilisateur avec rôles (simple / company).

- Créer  un modèle Theater et une API pour créer des salles.

- Connecter le backend à des tests unitaires et fixtures.

- Les tests vérifient création d’utilisateur, profil, salle et réservation.

Fonctionne avec pytest : uv run pytest
