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
            district = serializer.save()

            # Store the district in Elasticsearch
            es.index(index='districts', id=district.id, body={
                'id': district.id,
                'name': district.name,
                'description': district.description
            })

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class DistrictSearchView(APIView):
    def get(self, request, format=None):
        name = request.query_params.get('name', None)
        if name is not None:
            result = es.search(index='districts', body={
                "query":{
                "match":{
                "name":name
                }
                }
            })

            hits = result.get('hits',{}).get('hits',[])
            districts = []
            for hit in hits:
                district = hit.get('_source',{})
                districts.append(district)
            
            return Response(districts, status=status.HTTP_200_OK)
        else:
            result = es.search(index="districts", body={
                "query":{
                "match_all":{}
                }
            })

            hits = result.get('hits',{}).get('hits',[])
            districts = []
            for hit in hits:
                district = hit.get('_source',{})
                districts.append(district)
            
            return Response(districts, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)