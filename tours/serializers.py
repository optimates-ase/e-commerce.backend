from rest_framework import serializers
from rest_framework.fields import CharField, EmailField

from . import models
from .models import Tour


class ContactSerializer(serializers.ModelSerializer):
    name = CharField(source="title", required=True)
    message = CharField(source="description", required=True)
    email = EmailField(required=True)

    class Meta:
        model = models.Contact
        fields = ("name", "email", "message")


class TourSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tour
        fields = '__all__'
