from django.db import models


class Provider(models.Model):
    firstname = models.CharField(max_length=255)
    lastname = models.CharField(max_length=255)
    birthdate = models.DateField()
    email_address = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=255)
    languages_spoken = models.CharField(max_length=255)
    rating = models.DecimalField(max_digits=3, decimal_places=2, default=0.00)
    residence_street = models.CharField(max_length=255)
    residence_zip = models.CharField(max_length=255)
    residence_city = models.CharField(max_length=255)
    residence_country = models.CharField(max_length=255)
    access_token = models.CharField(max_length=255)
    refresh_token = models.CharField(max_length=255)
