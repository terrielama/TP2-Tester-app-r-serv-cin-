# ---- Mock pour l'API Gaumont ----

def book_seat(theater_name, movie_name, date):
    """
    Simule la réservation d'une séance Gaumont.
    Toujours renvoie succès pour les tests.
    """
    return {
        "success": True,
        "provider": "Gaumont",
        "theater_name": theater_name,
        "movie_name": movie_name,
        "date": date,
    }