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


class TourViewSet(views.ModelViewSet):
    queryset = Tour.objects.all()
    serializer_class = TourSerializer

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        # Store the tour in Elasticsearch
        tour_id = str(serializer.data.get('id'))
        tour = Tour.objects.get(id=tour_id)
        body = {'id': tour.id, 'name': tour.name, 'description': tour.description,
                'price': tour.price, 'date': tour.date, 'minOfParticipants': tour.minOfParticipants,
                'rating': tour.rating, 'numOfRatings': tour.numOfRatings}
        es.index(index='tours', id=tour_id, body=body)

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=201, headers=headers)

    def update(self, request, pk=None):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        # Update the tour in Elasticsearch
        tour_id = str(pk)
        tour = Tour.objects.get(id=tour_id)
        body = {'id': tour.id, 'name': tour.name, 'description': tour.description,
                'price': tour.price, 'date': tour.date, 'minOfParticipants': tour.minOfParticipants,
                'rating': tour.rating, 'numOfRatings': tour.numOfRatings}
        es.update(index='tours', id=tour_id, body={'doc': body})

        if getattr(tour, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the tour.
            tour._prefetched_objects_cache = {}

        return Response(serializer.data)

    def destroy(self, request, pk=None):
        tour_id = str(pk)

        # Delete the tour from Elasticsearch
        es.delete(index='tours', id=tour_id)

        return super().destroy(request, pk)

    def retrieve(self, request, pk=None):
        # Retrieve the tour from Elasticsearch
        tour_id = str(pk)
        result = es.get(index='tours', id=tour_id)
        tour = Tour(id=result['_source']['id'], name=result['_source']['name'],
                    description=result['_source']['description'], price=result['_source']['price'],
                    date=result['_source']['date'], minOfParticipants=result['_source']['minOfParticipants'],
                    rating=result['_source']['rating'], numOfRatings=result['_source']['numOfRatings'])
        serializer = TourSerializer(tour)
        return Response(serializer.data)
