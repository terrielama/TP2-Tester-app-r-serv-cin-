# TP2: Tester une application de réservation de cinéma


Groupe : Mathilde DELEKTA
		 Wallen JEAN MARIE ALPHONSINE
		 Terrie LAMA

 # Activer l'env :
  .venv\Scripts\activate

  # Installe les packages
uv sync

# Créer la base de données
uv run python manage.py makemigrations
uv run python manage.py migrate

# Run les test
uv run pytest
