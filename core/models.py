from django.contrib.auth.models import User
from django.db import models


# Notre modèle d'utilisateur
class BookUser(models.Model):
    # Le modèle User built-in for authentification
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # On n'hérite pas du modèle en le super-chargeant:
    # On créerait un super objet avec plein de rôle
    #
    is_company = models.BooleanField(default=False)
    # Là, il y a le Django User pour gérer l'authentification
    # Et noter BookUser pour gérer toutes les informations qu'on veut
    # enregistrer sur l'utilisateur

    @property
    def name(self):
        return self.user.username

    @property
    def email(self):
        return self.user.email


# -------- Theater model --------

class Theater(models.Model):
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)

    # Propriétaire de la salle
    owner = models.ForeignKey(BookUser, on_delete=models.CASCADE)

    def __str__(self):
        return self.name