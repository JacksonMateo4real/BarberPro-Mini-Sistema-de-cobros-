from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class User(AbstractUser):

    ROLE_CHOICES = (
        ('owner', 'Owner'),
        ('barber', 'Barber'),
    )

    phone_number = phone_number = models.CharField(
        max_length=15,
        blank=False,
        null=False
    )
    role = models.CharField(
        max_length=10,
        choices=ROLE_CHOICES
    )

    def __str__(self):
        return f"{self.first_name} {self.last_name}"