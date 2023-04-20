from django.db import models


class Provider(models.Model):
    from tours.models import Tour

    firstname = models.CharField(max_length=255)
    lastname = models.CharField(max_length=255)
    birthdate = models.DateField()
    email_address = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=255)
    languages_spoken = models.CharField(max_length=255)
    rating = models.DecimalField(max_digits=2, decimal_places=1, default=0.0)
    num_of_ratings = models.IntegerField(default=0)
    residence_street = models.CharField(max_length=255)
    residence_zip = models.CharField(max_length=255)
    residence_city = models.CharField(max_length=255)
    residence_country = models.CharField(max_length=255)
    access_token = models.CharField(max_length=255)
    refresh_token = models.CharField(max_length=255)
    provided_tours = models.ManyToManyField(Tour, related_name='providers')
