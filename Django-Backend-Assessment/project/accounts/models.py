from django.db import models
from django.db.models.functions import Lower


class Account(models.Model):
    name = models.CharField(max_length=20)
    email = models.EmailField(max_length=100)
    phone_number = models.CharField(max_length=10, unique=True)
    password = models.CharField(max_length=128)

    class Meta:
        constraints = [
            models.UniqueConstraint(Lower("email"), name="account_email_lower_unique"),
        ]
