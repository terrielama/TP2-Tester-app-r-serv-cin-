#TP – Gestion de Cinéma avec Django et Tests Automatisés

##A faire :

1. Partie tests Gherkin
Définir les scénarios pour les fonctionnalités principales :
	- Création d’utilisateur et séparation des rôles (user_bob / user_company)
	- Création de salle de cinéma (Theater)
	- Ajout de séances (Showtime)
	- Réservation de séances avec mock des APIs (MK2, UGC, Gaumont)
	- Ces scénarios ont été traduits en tests automatisés avec pytest et fixtures Django.

2. Partie Implémentation
Modèles (core/models.py) :
	- BookUser → profil utilisateur avec champ is_company
	- Theater → nom, adresse, propriétaire
	- Showtime → film, théâtre, date/heure, fournisseur
	- Fixtures (core/tests/fixtures.py) :
	- user_bob → utilisateur classique
	- user_company → utilisateur propriétaire de cinéma


Views (core/views.py) :
	- create_theater → création d’une salle par un propriétaire
	- create_showtime → création d’une séance pour un film
	- list_showtimes_for_movie → liste des séances disponibles pour un film
	- book_movie → réservation de séances (mock API pour tests)

URLs (core/urls.py) :
	- /core/theater/create/ → create_theater
	- /core/showtime/create/ → create_showtime
	- /core/showtimes/ → list_showtimes_for_movie
	- /core/book_movie/ → réservation de séances

3. Partie Tests unitaires
Tests fonctionnels avec pytest et Django :
	- Création d’utilisateur et rôle propriétaire vs utilisateur classique
	- Création de salles et séances
	- Réservation de séances avec mock des APIs externes
	- Vérification des statuts HTTP et des données retournées
	- Gestion des dates avec make_aware pour éviter les conflits timezone.

------------------------------------------------------------

Fonctionnalités actuelles :

1) Un propriétaire de cinéma peut créer ses salles (Theater) et ajouter des séances (Showtime).

2) Un utilisateur classique peut :
	- Voir la liste des films à l’affiche
	- Voir pour chaque film les salles qui le diffusent et leurs horaires
	- Réserver une séance (via l’API simulée des fournisseurs)

------------------------------------------------------------

Implémentation #1 : Gestion des rôles et création de salles

Étape 1 : Séparer les rôles utilisateurs (user_bob vs user_company)

Étape 2 : Créer une salle de cinéma (Theater)

Étape 3 : Ajouter les séances (Showtime)

------------------------------------------------------------

Implémentation #2 : Déclarer une salle de cinéma

Permet à un utilisateur propriétaire de déclarer ses salles via /core/theater/create/.

Les tests unitaires vérifient la création correcte de la salle et l’association avec le propriétaire.

------------------------------------------------------------

Groupe : Mathilde DELEKTA
		 Wallen JEAN MARIE ALPHONSINE
		 Terrie LAMA

------------------------------------------------------------

 - Activer l'env :
  .venv\Scripts\activate

 - Installe les packages
uv sync

- Créer la base de données
uv run python manage.py makemigrations
uv run python manage.py migrate

- Run les test
uv run pytest






