from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.http import JsonResponse
import json
import json
from core.models import Theater, Showtime
from core import models
from external_apis import mk2
from django.utils.dateparse import parse_datetime
from external_apis import mk2, ugc, gaumont


# ---------- Création d'un utilisateur ----------
def create_user(request):
    if request.method == "POST":
        data = json.loads(request.body)

        # Vérifie que l'email est fourni
        if not data.get("email"):
            return JsonResponse({"error": "Email required"}, status=400)

        # Création du User Django (authentification)
        user = models.User.objects.create_user(
            username=data["name"],
            email=data["email"],
            password=data["password"],
        )
        user.save()

        # Création du BookUser
        book_user = models.BookUser(user=user)
        book_user.save()

        #  Retour des infos utilisateur 
        return JsonResponse(
            {
                "username": book_user.name,
                "email": book_user.email,
                "id": book_user.id,
            },
            status=201,
        )


#  Récupérer un utilisateur par ID 
def get_user(request):
    user_id = request.GET.get("id")

    # Vérifie que l'id est fourni 
    if not user_id:
        return JsonResponse({"error": "id required"}, status=400)

    try:
        user = models.BookUser.objects.get(pk=user_id)

        # Retour des infos utilisateur 
        return JsonResponse(
            {
                "username": user.name,
                "email": user.email,
                "id": user.id,
            }
        )

    except models.BookUser.DoesNotExist:
        return JsonResponse({"error": "not found"}, status=404)


# ---------- Profil de l'utilisateur connecté ----------
def get_my_profile(request):
    # Vérifie que l'utilisateur est connecté
    if not request.user.is_authenticated:
        return JsonResponse(
            {"error": "Must be authenticated to see your profile"},
            status=403,
        )

    # Récupère le BookUser lié au User
    user = request.user.bookuser

    #  Retour des infos du profil
    return JsonResponse(
        {
            "username": user.name,
            "email": user.email,
            "id": user.id,
        }
    )


# ---- Connexion utilisateur ----
def login_view(request):
    data = json.loads(request.body)

    username = data.get("username")
    password = data.get("password")

    # Vérifie que username et password sont fournis
    if not username or not password:
        return JsonResponse(
            {"detail": "Username and password are required."},
            status=400,
        )

    #  Authentification
    user = authenticate(request, username=username, password=password)

    if user is not None:
        login(request, user)  # Création de la session
        return JsonResponse({"message": "Login successful"})
    else:
        return JsonResponse({"detail": "Invalid credentials"}, status=401)


# Réserver une séance (appel API externe MK2)

def book_movie(request):
    if not request.user.is_authenticated:
        return JsonResponse({"error": "Authentication required"}, status=403)

    if request.method != "POST":
        return JsonResponse({"error": "Method not allowed"}, status=405)

    data = json.loads(request.body)
    showtime_id = data.get("showtime_id")
    if not showtime_id:
        return JsonResponse({"error": "showtime_id required"}, status=400)

    try:
        showtime = Showtime.objects.get(pk=showtime_id)
    except Showtime.DoesNotExist:
        return JsonResponse({"error": "Showtime not found"}, status=404)

    # Appel au bon fournisseur selon le champ provider
    provider_api = {
        "MK2": mk2,
        "UGC": ugc,
        "Gaumont": gaumont
    }.get(showtime.provider)

    if not provider_api:
        return JsonResponse({"error": "Unknown provider"}, status=400)

    result = provider_api.book_seat(
        theater_name=showtime.theater.name,
        movie_name=showtime.movie_name,
        date=str(showtime.start_time)
    )

    return JsonResponse(result)
    
# ---- Les utilisateurs de type "compagnie" puissent créer de nouvelles salles de cinéma ------
def create_theater(request):
    # Vérification méthode POST 
    if request.method != "POST":
        return JsonResponse({"error": "Method not allowed"}, status=405)

    # Vérification de l'authentification 
    if not request.user.is_authenticated:
        return JsonResponse({"error": "Authentication required"}, status=403)

    # Vérification que l'utilisateur est une compagnie
    book_user = request.user.bookuser
    if not book_user.is_company:
        return JsonResponse({"error": "Only company users can create theaters"}, status=403)

    # Lecture du payload JSON
    data = json.loads(request.body)
    name = data.get("name")
    address = data.get("address")

    if not name or not address:
        return JsonResponse({"error": "Name and address are required"}, status=400)

    # Création du théâtre 
    theater = Theater.objects.create(
        name=name,
        address=address,
        owner=book_user
    )

    # Réponse JSON 
    return JsonResponse({
        "id": theater.id,
        "name": theater.name,
        "address": theater.address,
    }, status=201)


# ---------- Company crée séance ---------
def create_showtime(request):
    # Vérif POST
    if request.method != "POST":
        return JsonResponse({"error": "Method not allowed"}, status=405)

    if not request.user.is_authenticated:
        return JsonResponse({"error": "Authentication required"}, status=403)

    book_user = request.user.bookuser
    if not book_user.is_company:
        return JsonResponse({"error": "Only company users can create showtimes"}, status=403)

    # Lecture JSON
    data = json.loads(request.body)
    theater_id = data.get("theater_id")
    movie_name = data.get("movie_name")
    start_time = parse_datetime(data.get("start_time"))
    provider = data.get("provider", "MK2")  # par défaut MK2

    if not theater_id or not movie_name or not start_time:
        return JsonResponse({"error": "theater_id, movie_name and start_time required"}, status=400)

    # Vérif que la salle appartient à ce company
    try:
        theater = Theater.objects.get(pk=theater_id, owner=book_user)
    except Theater.DoesNotExist:
        return JsonResponse({"error": "Theater not found or not owned"}, status=404)

    #  Création de la séance
    showtime = Showtime.objects.create(
        theater=theater,
        movie_name=movie_name,
        start_time=start_time,
        provider=provider
    )

    return JsonResponse({
        "id": showtime.id,
        "movie_name": showtime.movie_name,
        "theater": theater.name,
        "start_time": showtime.start_time.isoformat(),
        "provider": showtime.provider
    }, status=201)




# ---- Utilisateur normal liste films ----
def list_movies(request):
    # Tous les films avec leurs séances et salles
    showtimes = Showtime.objects.select_related('theater').all()
    movies = {}

    for s in showtimes:
        if s.movie_name not in movies:
            movies[s.movie_name] = []

        movies[s.movie_name].append({
            "theater": s.theater.name,
            "address": s.theater.address,
            "start_time": s.start_time.isoformat(),
            "provider": getattr(s.theater, "provider", "Unknown")
        })

    return JsonResponse(movies)


# ---------- retourner toutes les salles qui le diffusent avec les horaires ----------
def list_showtimes_for_movie(request):
    # Récupérer le nom du film depuis les query params
    movie_name = request.GET.get("movie_name")
    if not movie_name:
        return JsonResponse({"error": "movie_name is required"}, status=400)

    # Filtrer les séances du film
    showtimes = Showtime.objects.filter(movie_name=movie_name).select_related('theater')

    # Construire la réponse JSON
    data = [
        {
            "theater_name": s.theater.name,
            "address": s.theater.address,
            "start_time": s.start_time.strftime("%Y-%m-%d %H:%M:%S"),
            "provider": s.provider
        }
        for s in showtimes
    ]
    return JsonResponse(data, safe=False)