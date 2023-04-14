from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Geo
from elasticsearch import Elasticsearch

es = Elasticsearch()

# Create your views here.
class GeoSearchView(APIView):
    def get(self, format=None):
        res = es.search(index='geo_data', body={
            "query":{
                "match":{
                    "name":'gadm41_BLZ_0'
                }
            }
        })

        hits = res.get('hits',{}).get('hits',[])
        geos = []
        for hit in hits:
            geos.append(hit.get('_source',{}))

        return Response(geos[0], status=status.HTTP_200_OK)

class GeoDistrictsSearchView(APIView):
    def get(self, format=None):
        res = es.search(index='geo_data', body={
            "query":{
                "match":{
                    "name":'gadm41_BLZ_1'
                }
            }
        })

        hits = res.get('hits',{}).get('hits',[])
        geos = []
        for hit in hits:
            geos.append(hit.get('_source',{}))

        return Response(geos[0], status=status.HTTP_200_OK)