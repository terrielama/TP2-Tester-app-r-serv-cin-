from django.contrib.auth.models import User
from django.db import models


class UserType(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_type')
    is_company = models.BooleanField(default=False)
