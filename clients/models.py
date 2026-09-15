from django.db import models

# Create your models here.
class Client(models.Model):
    full_name = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=15, blank=True, null=True)


    def __str__(self):
        return f"{self.full_name}"
