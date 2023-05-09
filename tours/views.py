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

es = Elasticsearch("http://elasticsearch:9200")


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


class RandomToursAPIView(APIView):
    def get(self, request):
        page = int(request.query_params.get("page", 1))
        page_size = int(request.query_params.get("page_size", 10))

        start = (page - 1) * page_size
        end = start + page_size

        tours = es.search(index="tours", size=10000)

        total_count = tours["hits"]["total"]["value"]
        tours = tours["hits"]["hits"]
        random.shuffle(tours)

        tours = tours[start:end]

        response = {
            "page": page,
            "page_size": page_size,
            "total_count": total_count,
            "data": [],
        }

        for tour in tours:
            tour_data = tour["_source"]
            tour_data["id"] = tour["_id"]
            response["data"].append(tour_data)

        return Response(response, status=status.HTTP_200_OK)


class TourAPIView(APIView):
    def post(self, request, format=None):
        serializer = TourSerializer(data=request.data)
        my_data = request.data
        if serializer.is_valid():
            body = {
                "name": my_data.get("name", None),
                "description": my_data.get("description", None),
                "price": my_data.get("price", None),
                "date": my_data.get("date", None),
                "min_of_participants": my_data.get("min_of_participants", None),
                "rating": None,
                "num_of_ratings": 0,
                "language_offered": my_data.get("language_offered", None),
            }
            tour_es = es.index(
                index="tours",
                body=body,
            )
            return Response(tour_es, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, format=None):
        tour_id = request.query_params.get("id", None)
        tour = es.get(index="tours", id=tour_id)

        serializer = TourSerializer(data=tour["_source"])
        if serializer.is_valid():
            return Response(tour, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, format=None):
        tour_id = request.query_params.get("id", None)

        my_data = request.data

        if my_data is not None:
            body = {}

            if my_data.get("name") is not None:
                body["name"] = my_data["name"]
            if my_data.get("description") is not None:
                body["description"] = my_data["description"]
            if my_data.get("price") is not None:
                body["price"] = my_data["price"]
            if my_data.get("date") is not None:
                body["date"] = my_data["date"]
            if my_data.get("min_of_participants") is not None:
                body["min_of_participants"] = my_data["min_of_participants"]
            if my_data.get("language_offered") is not None:
                body["language_offered"] = my_data["language_offered"]

            tour_es = es.index(
                index="tours",
                id=tour_id,
                body=body,
            )
            return Response(tour_es, status=status.HTTP_201_CREATED)
        return Response(f"bad request: {tour_es}", status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, format=None):
        tour_id = request.query_params.get("id", None)
        response = es.delete(index="tours", id=tour_id)
        return Response(response, status=status.HTTP_204_NO_CONTENT)


class TourRatingAPIView(APIView):
    def post(self, request):
        tour_id = request.query_params.get("id", None)
        if not tour_id:
            return Response(
                {"message": "Tour ID is required"}, status=status.HTTP_400_BAD_REQUEST
            )
        try:
            tour = es.get(index="tours", id=tour_id)
        except:
            return Response(
                {"message": "Tour not found"}, status=status.HTTP_404_NOT_FOUND
            )

        rating = request.query_params.get("rating")

        current_num_of_ratings = tour["_source"]["num_of_ratings"]
        current_rating = tour["_source"]["rating"]
        new_num_of_ratings = current_num_of_ratings + 1
        new_rating = (
            current_rating * current_num_of_ratings + float(rating)
        ) / new_num_of_ratings

        es.update(
            index="tours",
            id=tour_id,
            body={"doc": {"rating": new_rating, "num_of_ratings": new_num_of_ratings}},
        )
        return Response(
            {"message": "Tour rated successfully"}, status=status.HTTP_201_CREATED
        )
