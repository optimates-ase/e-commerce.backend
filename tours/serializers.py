from rest_framework import serializers
from rest_framework.fields import CharField, EmailField

from . import models


class ContactSerializer(serializers.ModelSerializer):
    name = CharField(source="title", required=True)
    message = CharField(source="description", required=True)
    email = EmailField(required=True)

    class Meta:
        model = models.Contact
        fields = ("name", "email", "message")


class TourSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Tour
        fields = ['id', 'name', 'description', 'price', 'date',
                  'min_of_participants', 'rating', 'num_of_ratings']
