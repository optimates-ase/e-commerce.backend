from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import District
from .serializers import DistrictSerializer
from elasticsearch import Elasticsearch

es = Elasticsearch()

class DistrictCreateView(APIView):
    def post(self, request, format=None):
        serializer = DistrictSerializer(data=request.data)
        if serializer.is_valid():
            driver = serializer.save()

            # Store the driver in Elasticsearch
            es.index(index='drivers', id=driver.id, body={
                'id': driver.id,
                'name': driver.name,
                'description': driver.description
            })

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
