from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from elasticsearch import Elasticsearch
from customers.serializers import CustomerSerializer

es = Elasticsearch("http://elasticsearch:9200")


class CustomerAPIView(APIView):

    def post(self, request, format=None):
        serializer = CustomerSerializer(data=request.data)
        my_data = request.data
        # if serializer.is_valid():
        if my_data is not None:

            customer_es = es.index(index='customers', body={
                'firstname': my_data['firstname'],
                'lastname': my_data['lastname'],
                'birthdate': my_data['birthdate'],
                'email_address': my_data['email_address'],
                'phone_number': my_data['phone_number'],
                'billing_street': my_data['billing_street'],
                'billing_zip': my_data['billing_zip'],
                'billing_city': my_data['billing_city'],
                'billing_country': my_data['billing_country'],
                'residence_street': my_data['residence_street'],
                'residence_zip': my_data['residence_zip'],
                'residence_city': my_data['residence_city'],
                'residence_country': my_data['residence_country'],
                'access_token': my_data['access_token'],
                'refresh_token': my_data['refresh_token'],
            })
            return Response(customer_es, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, format=None):
        customer_id = request.query_params.get('id', None)
        customer = es.get(index='customers', id=customer_id)

        serializer = CustomerSerializer(data=customer['_source'])
        # if serializer.is_valid():
        if customer is not None:
            return Response(customer, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, format=None):
        customer_id = request.query_params.get('id', None)

        my_data = request.data

        if my_data is not None:
            customer_es = es.index(index='customers', id=customer_id, body={
                'firstname': my_data['firstname'],
                'lastname': my_data['lastname'],
                'birthdate': my_data['birthdate'],
                'email_address': my_data['email_address'],
                'phone_number': my_data['phone_number'],
                'billing_street': my_data['billing_street'],
                'billing_zip': my_data['billing_zip'],
                'billing_city': my_data['billing_city'],
                'billing_country': my_data['billing_country'],
                'residence_street': my_data['residence_street'],
                'residence_zip': my_data['residence_zip'],
                'residence_city': my_data['residence_city'],
                'residence_country': my_data['residence_country'],
                'access_token': my_data['access_token'],
                'refresh_token': my_data['refresh_token'],
            })
            return Response(customer_es, status=status.HTTP_201_CREATED)
        return Response(f"bad request: {customer_es}", status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, format=None):
        customer_id = request.query_params.get('id', None)
        response = es.delete(index='customers', id=customer_id)
        return Response(response, status=status.HTTP_204_NO_CONTENT)
