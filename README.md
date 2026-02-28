# TP2: Tester une application de réservation de cinéma

A faire :
1. Partie tests Gherkin
2. Partie Implémentation : Modèles, Fixtures, Views, URLs, Tests unitaires
3. Fonctionnalités actuelles

Implémentation #1: Un utilisateur propriétaire de salle de cinéma :
			Étape 1 : Séparer les rôles utilisateurs
			Étape 2 : Créer une salle de cinéma
			Étape 3 : Ajouter les séances

Implémentation #2: Déclarer une salle de cinéma
On veut maintenant qu'un utilisateur propriétaire de salles puisse déclarer ses salles.
-------------------------

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


