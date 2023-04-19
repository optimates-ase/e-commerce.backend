from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from elasticsearch import Elasticsearch
from providers.serializers import ProviderSerializer

es = Elasticsearch()


class ProviderAPIView(APIView):

    def post(self, request, format=None):
        serializer = ProviderSerializer(data=request.data)
        my_data = request.data
        if serializer.is_valid():

            provider_es = es.index(index='providers', body={
                'firstname': my_data['firstname'],
                'lastname': my_data['lastname'],
                'birthdate': my_data['birthdate'],
                'email_address': my_data['email_address'],
                'phone_number': my_data['phone_number'],
                'languages_spoken': my_data['languages_spoken'],
                'rating': my_data['rating'],
                'residence_street': my_data['residence_street'],
                'residence_zip': my_data['residence_zip'],
                'residence_city': my_data['residence_city'],
                'residence_country': my_data['residence_country'],
                'access_token': my_data['access_token'],
                'refresh_token': my_data['refresh_token'],
            })
            return Response(provider_es, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, format=None):
        provider_id = request.query_params.get('id', None)
        provider = es.get(index='providers', id=provider_id)

        serializer = ProviderSerializer(data=provider['_source'])
        if serializer.is_valid():
            return Response(provider, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, id, format=None):
        provider_id = request.query_params.get('id', None)

        my_data = request.data

        if my_data is not None:
            provider_es = es.index(index='providers', id=provider_id, body={
                'firstname': my_data['firstname'],
                'lastname': my_data['lastname'],
                'birthdate': my_data['birthdate'],
                'email_address': my_data['email_address'],
                'phone_number': my_data['phone_number'],
                'languages_spoken': my_data['languages_spoken'],
                'rating': my_data['rating'],
                'residence_street': my_data['residence_street'],
                'residence_zip': my_data['residence_zip'],
                'residence_city': my_data['residence_city'],
                'residence_country': my_data['residence_country'],
                'access_token': my_data['access_token'],
                'refresh_token': my_data['refresh_token'],
            })
            return Response(provider_es, status=status.HTTP_201_CREATED)
        return Response(f"bad request: {provider_es}", status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, format=None):
        provider_id = request.query_params.get('id', None)
        response = es.delete(index='providers', id=provider_id)
        return Response(response, status=status.HTTP_204_NO_CONTENT)
