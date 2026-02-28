from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.http import JsonResponse
import json
import json
from core.models import Theater
from core import models
from external_apis import mk2


# ---- Création d'un utilisateur ----
def create_user(request):
    if request.method == "POST":
        data = json.loads(request.body)

        # ---- Vérifie que l'email est fourni ----
        if not data.get("email"):
            return JsonResponse({"error": "Email required"}, status=400)

        # ---- Création du User Django (authentification) ----
        user = models.User.objects.create_user(
            username=data["name"],
            email=data["email"],
            password=data["password"],
        )
        user.save()

        # ---- Création du BookUser ----
        book_user = models.BookUser(user=user)
        book_user.save()

        # ---- Retour des infos utilisateur ----
        return JsonResponse(
            {
                "username": book_user.name,
                "email": book_user.email,
                "id": book_user.id,
            },
            status=201,
        )


# ---- Récupérer un utilisateur par ID ----
def get_user(request):
    user_id = request.GET.get("id")

    # ---- Vérifie que l'id est fourni ----
    if not user_id:
        return JsonResponse({"error": "id required"}, status=400)

    try:
        user = models.BookUser.objects.get(pk=user_id)

        # ---- Retour des infos utilisateur ----
        return JsonResponse(
            {
                "username": user.name,
                "email": user.email,
                "id": user.id,
            }
        )

    except models.BookUser.DoesNotExist:
        return JsonResponse({"error": "not found"}, status=404)


# ---- Profil de l'utilisateur connecté ----
def get_my_profile(request):
    # Vérifie que l'utilisateur est connecté ----
    if not request.user.is_authenticated:
        return JsonResponse(
            {"error": "Must be authenticated to see your profile"},
            status=403,
        )

    # ---- Récupère le BookUser lié au User ----
    user = request.user.bookuser

    # ---- Retour des infos du profil ----
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

    # ---- Vérifie que username et password sont fournis ----
    if not username or not password:
        return JsonResponse(
            {"detail": "Username and password are required."},
            status=400,
        )

    # ---- Authentification ----
    user = authenticate(request, username=username, password=password)

    if user is not None:
        login(request, user)  # Création de la session
        return JsonResponse({"message": "Login successful"})
    else:
        return JsonResponse({"detail": "Invalid credentials"}, status=401)


# ---- Réserver une séance (appel API externe MK2)
def book_movie(request):
    # Vérifie que l'utilisateur est connecté
    if not request.user.is_authenticated:
        return JsonResponse(
            {"error": "Must be authenticated to book a seat"},
            status=403,
        )

    if request.method == "POST":
        data = json.loads(request.body)

        # Appel à l'API externe MK2
        return JsonResponse(
            mk2.book_seat(
                theater_name="MK2 Gambetta",
                movie_name=data["movie_name"],
                date=data["date"],
            )
        )
    
# ---- Les utilisateurs de type "compagnie" puissent créer de nouvelles salles de cinéma ------

def create_theater(request):
    # ---- Vérification méthode POST ----
    if request.method != "POST":
        return JsonResponse({"error": "Method not allowed"}, status=405)

    # ---- Vérification de l'authentification ----
    if not request.user.is_authenticated:
        return JsonResponse({"error": "Authentication required"}, status=403)

    # ---- Vérification que l'utilisateur est une compagnie ----
    book_user = request.user.bookuser
    if not book_user.is_company:
        return JsonResponse({"error": "Only company users can create theaters"}, status=403)

    # ---- Lecture du payload JSON ----
    data = json.loads(request.body)
    name = data.get("name")
    address = data.get("address")

    if not name or not address:
        return JsonResponse({"error": "Name and address are required"}, status=400)

    # ---- Création du théâtre ----
    theater = Theater.objects.create(
        name=name,
        address=address,
        owner=book_user
    )

    # ---- Réponse JSON ----
    return JsonResponse({
        "id": theater.id,
        "name": theater.name,
        "address": theater.address,
    }, status=201)