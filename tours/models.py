from django.db import models
from django_extensions.db.models import (
    ActivatorModel,
    TimeStampedModel,
    TitleDescriptionModel,
)

from utils.model_abstacts import Model


class Contact(TimeStampedModel, ActivatorModel, TitleDescriptionModel, Model):
    class Meta:
        verbose_name_plural = "Contacts"

    email = models.EmailField(verbose_name="Email")

    def __str__(self) -> str:
        return self.title


# Create your models here.
class Tour(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField()
    min_of_participants = models.PositiveIntegerField()
    rating = models.DecimalField(max_digits=3, decimal_places=2, default=0.00)
    num_of_ratings = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"name={self.name}, description={self.description}, price={self.price}, date={self.date}, min_of_participants={self.min_of_participants}, rating={self.rating}, num_of_ratings={self.num_of_ratings})"
