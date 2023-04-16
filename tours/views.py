from .serializers import TourSerializer
from rest_framework import status
from json import JSONDecodeError

from django.http import JsonResponse
from rest_framework import status, views
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.views import APIView
from random import shuffle
from .models import Tour
from .serializers import TourSerializer, ContactSerializer
from elasticsearch import Elasticsearch
import random
from rest_framework.pagination import PageNumberPagination


es = Elasticsearch()


class ContactAPIView(views.APIView):
    """
    A simple APIView to create contact entries
    """

    serializer_class = ContactSerializer

    def get_serializer_context(self):
        return {
            "request": self.request,
            "format": self.format_kwarg,
            "view": self,
        }

    def get_serializer(self, *args, **kwargs):
        kwargs["context"] = self.get_serializer_context()
        return self.serializer_class(*args, **kwargs)

    def post(self, request):
        try:
            parser = JSONParser()
            data = parser.parse(request)
            serializer = ContactSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except JSONDecodeError:
            return JsonResponse(
                {
                    "result": "Error",
                    "message": "JSON Decoding Error",
                },
                status=status.HTTP_400_BAD_REQUEST,
            )


class RandomTourAPIView(APIView):
    def list(self, request):
        queryset = Tour.objects.all()
        random_tours = sorted(queryset, key=lambda x: random.random())
        paginator = RandomToursPagination()
        result_page = paginator.paginate_queryset(random_tours, request)
        serializer = TourSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)


class RandomToursPagination(PageNumberPagination):
    page_size = 10
    max_page_size = 100
    page_size_query_param = 'page_size'


class TourAPIView(APIView):
    """
    A simple APIView for creating, updating, and deleting tours.
    """

    def post(self, request, format=None):

        serializer = TourSerializer(data=request.data)
        if serializer.is_valid():
            tour = serializer.save()

            # Store the tour in Elasticsearch
            es.index(index='tours', body={
                'name': tour.name,
                'description': tour.description,
                'price': tour.price,
                'date': tour.date,
                'min_of_participants': tour.min_of_participants,
                'rating': tour.rating,
                'num_of_ratings': tour.num_of_ratings,
            })

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, pk=None, format=None):
        # Get a single tour from Elasticsearch
        tour = es.get(index='tours', id=pk)

        # Return the serialized tour data
        serializer = TourSerializer(data=tour['_source'])
        if serializer.is_valid():
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk=None, format=None):
        # Retrieve the tour from Elasticsearch
        tour = es.get(index='tours', id=pk)

        # Update the tour object with the new data
        serializer = TourSerializer(instance=tour['_source'], data=request.data)
        if serializer.is_valid():
            tour = serializer.save()

            # Update the tour in Elasticsearch
            es.index(index='tours', id=pk, body={
                'id': tour.id,
                'name': tour.name,
                'description': tour.description,
                'price': tour.price,
                'date': tour.date,
                'min_of_participants': tour.min_of_participants,
                'rating': tour.rating,
                'num_of_ratings': tour.num_of_ratings,
            })
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk=None, format=None):
        # Delete the tour from Elasticsearch
        es.delete(index='tours', id=pk)

        # Delete the tour object from the database
        try:
            tour = Tour.objects.get(pk=pk)
            tour.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Tour.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
