from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Weather
from elasticsearch import Elasticsearch

es = Elasticsearch("http://elasticsearch:9200")

# Create your views here.


class WeatherSearchView(APIView):
    def get(self, format=None):
        res = es.search(index='weather', body={
            "query": {
                "match_all": {}
            }
        })

        hits = res.get('hits', {}).get('hits', [])
        jsons = []
        for hit in hits:
            jsons.append(hit.get('_source', {}))

        return Response(jsons[0], status=status.HTTP_200_OK)


class ClimateSearchView(APIView):
    def get(self, request, format=None):
        month = request.query_params.get('month', None)
        res = es.search(index='climate', body={
            "query": {
                "wildcard": {
                "month": {
                    "value": f"*{month}*"
                }
                }
            }
        })

        hits = res.get('hits', {}).get('hits', [])
        geos = []
        for hit in hits:
            geos.append(hit.get('_source', {}))

        return Response(geos[0], status=status.HTTP_200_OK)
