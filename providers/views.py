from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from elasticsearch import Elasticsearch
from providers.serializers import ProviderSerializer

es = Elasticsearch("http://elasticsearch:9200")


class ProviderAPIView(APIView):
    def post(self, request, format=None):
        my_data = request.data

        body = {
            "firstname": my_data.get("firstname", None),
            "lastname": my_data.get("lastname", None),
            "birthdate": my_data.get("birthdate", None),
            "email_address": my_data.get("email_address", None),
            "phone_number": my_data.get("phone_number", None),
            "languages_spoken": my_data.get("languages_spoken", None),
            "rating": None,
            "num_of_ratings": 0,
            "residence_street": my_data.get("residence_street", None),
            "residence_zip": my_data.get("residence_zip", None),
            "residence_city": my_data.get("residence_city", None),
            "residence_country": my_data.get("residence_country", None),
            "access_token": my_data.get("access_token", None),
            "refresh_token": my_data.get("refresh_token", None),
        }

        provider_es = es.index(index="providers", body=body)

        return Response(provider_es, status=status.HTTP_201_CREATED)

    def get(self, request, format=None):
        provider_id = request.query_params.get("id", None)
        provider = es.get(index="providers", id=provider_id)

        serializer = ProviderSerializer(data=provider["_source"])

        if provider is not None:
            return Response(provider, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, format=None):
        provider_id = request.query_params.get("id", None)

        my_data = request.data

        if my_data is not None:
            body = {}
            if my_data.get("firstname") is not None:
                body["firstname"] = my_data["firstname"]
            if my_data.get("lastname") is not None:
                body["lastname"] = my_data["lastname"]
            if my_data.get("birthdate") is not None:
                body["birthdate"] = my_data["birthdate"]
            if my_data.get("email_address") is not None:
                body["email_address"] = my_data["email_address"]
            if my_data.get("phone_number") is not None:
                body["phone_number"] = my_data["phone_number"]
            if my_data.get("languages_spoken") is not None:
                body["languages_spoken"] = my_data["languages_spoken"]
            if my_data.get("residence_street") is not None:
                body["residence_street"] = my_data["residence_street"]
            if my_data.get("residence_zip") is not None:
                body["residence_zip"] = my_data["residence_zip"]
            if my_data.get("residence_city") is not None:
                body["residence_city"] = my_data["residence_city"]
            if my_data.get("residence_country") is not None:
                body["residence_country"] = my_data["residence_country"]
            if my_data.get("access_token") is not None:
                body["access_token"] = my_data["access_token"]
            if my_data.get("refresh_token") is not None:
                body["refresh_token"] = my_data["refresh_token"]

            provider_es = es.index(
                index="providers",
                id=provider_id,
                body=body,
            )
            return Response(provider_es, status=status.HTTP_201_CREATED)
        return Response(
            f"bad request: {provider_es}", status=status.HTTP_400_BAD_REQUEST
        )

    def delete(self, request, format=None):
        provider_id = request.query_params.get("id", None)
        response = es.delete(index="providers", id=provider_id)
        return Response(response, status=status.HTTP_204_NO_CONTENT)


class ProviderRatingAPIView(APIView):
    def post(self, request):
        provider_id = request.query_params.get("id", None)
        try:
            provider = es.get(index="providers", id=provider_id)
        except:
            return Response(
                {"message": "Provider not found"}, status=status.HTTP_404_NOT_FOUND
            )

        # Retrieve the new rating from the request body
        rating = request.data.get("rating")

        # Calculate the new average rating
        current_num_of_ratings = provider["_source"]["num_of_ratings"]
        current_rating = provider["_source"]["rating"]
        new_num_of_ratings = current_num_of_ratings + 1
        new_rating = (
            current_rating * current_num_of_ratings + rating
        ) / new_num_of_ratings

        # Update the Elasticsearch document with the new average rating and number of ratings
        es.update(
            index="providers",
            id=provider_id,
            body={"doc": {"rating": new_rating, "num_of_ratings": new_num_of_ratings}},
        )
        return Response(
            {"message": "Provider rated successfully"}, status=status.HTTP_201_CREATED
        )
