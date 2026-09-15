from django.db import models
from django.conf import settings
from clients.models import Client


class Sale(models.Model):

    SERVICE_TYPE_CHOICES = [
        ('haircut', 'Corte'),
        ('beard', 'Barba'),
        ('haircut_beard', 'Corte + Barba'),
        ('eyebrows', 'Cejas'),
        ('full', 'Full')
    ]

    PAYMENT_METHOD_CHOICES = [
        ('cash', 'Efectivo'),
        ('card', 'Tarjeta de crédito/débito'),
    ]

    SERVICE_PRICE = {
        'haircut': 15,
        'beard': 7,
        'haircut_beard': 22,
        'eyebrows': 5,
        'full': 27
    }

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='sales')
    client = models.ForeignKey(Client, on_delete=models.SET_NULL, null=True, blank=True)

    service_type = models.CharField(max_length=30, choices=SERVICE_TYPE_CHOICES)
    payment_method = models.CharField(max_length=30, choices=PAYMENT_METHOD_CHOICES)

    price = models.IntegerField()

    creation_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.client} - {self.service_type} - {self.price} Atendido por: {self.user.first_name}"