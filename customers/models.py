from django.db import models


class Customer(models.Model):
    firstname = models.CharField(max_length=255)
    lastname = models.CharField(max_length=255)
    birthdate = models.DateField()
    email_address = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=255)
    billing_street = models.CharField(max_length=255)
    billing_zip = models.CharField(max_length=255)
    billing_city = models.CharField(max_length=255)
    billing_country = models.CharField(max_length=255)
    residence_street = models.CharField(max_length=255)
    residence_zip = models.CharField(max_length=255)
    residence_city = models.CharField(max_length=255)
    residence_country = models.CharField(max_length=255)
    access_token = models.CharField(max_length=255)
    refresh_token = models.CharField(max_length=255)
