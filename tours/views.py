from .serializers import TourSerializer
from rest_framework import status
from json import JSONDecodeError

from django.http import JsonResponse
from rest_framework import status, views
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.views import APIView
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


es = Elasticsearch(['http://localhost:9200'])


class TourAPIView(APIView):

    def post(self, request, format=None):
        serializer = TourSerializer(data=request.data)
        my_data = request.data
        if serializer.is_valid():

            # Store the tour in Elasticsearch
            tour_es = es.index(index='tours', body={
                'name': my_data['name'],
                'description': my_data['description'],
                'price': my_data['price'],
                'date': my_data['date'],
                'min_of_participants': my_data['min_of_participants'],
                'rating': my_data['rating'],
                'num_of_ratings': my_data['num_of_ratings'],
            })

            return Response(tour_es, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, format=None):
        tour_id = request.query_params.get('id', None)
        tour = es.get(index='tours', id=tour_id)

        serializer = TourSerializer(data=tour['_source'])
        if serializer.is_valid():
            return Response(tour, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, format=None):
        tour_id = request.query_params.get('id', None)
        tour = es.get(index='tours', id=tour_id)

        my_data = request.data

        if my_data is not None:

            # Update the tour in Elasticsearch
            tour_es = es.index(index='tours', id=tour_id, body={
                'name': my_data['name'],
                'description': my_data['description'],
                'price': my_data['price'],
                'date': my_data['date'],
                'min_of_participants': my_data['min_of_participants'],
                'rating': my_data['rating'],
                'num_of_ratings': my_data['num_of_ratings'],
            })
            return Response(tour_es, status=status.HTTP_201_CREATED)
        return Response(f"bad request: {tour_es}", status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, format=None):
        tour_id = request.query_params.get('id', None)
        response = es.delete(index='tours', id=tour_id)
        return Response(response, status=status.HTTP_204_NO_CONTENT)
