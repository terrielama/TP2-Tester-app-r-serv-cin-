from django.contrib.auth.models import User
from django.db import models


class UserType(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_type')
    is_company = models.BooleanField(default=False)

    def json(self):
        return {
            "id": self.user.id,
            "username": self.user.username,
            "email": self.user.email,
            "is_company": self.is_company,
        }


class Theater(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='theaters')
    name = models.CharField(max_length=200)
    address = models.CharField(max_length=1_000)
