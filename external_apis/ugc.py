# ---- Mock pour l'API UGC ----

def book_seat(theater_name, movie_name, date):
    """
    Simule la réservation d'une séance UGC.
    Toujours renvoie succès pour les tests.
    """
    return {
        "success": True,
        "provider": "UGC",
        "theater_name": theater_name,
        "movie_name": movie_name,
        "date": date,
    }