from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from elasticsearch import Elasticsearch
from customers.serializers import CustomerSerializer
from customers.models import Customer
from tours.models import Tour

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
                'marked_tours': [],
                'booked_tours': []
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


class CustomerMarkingTourAPIView(APIView):
    def post(self, request):
        if request.query_params is not None:
            customer_id = request.query_params.get('customer_id', None)
            tour_id = request.query_params.get('tour_id', None)
            try:
                customer = es.get(index='customers', id=customer_id)
                tour = es.get(index='tours', id=tour_id)

                customer.marked_tours.add(tour)
                customer.save()
            except:
                return Response({'message': 'Customer or Tour not found'}, status=status.HTTP_404_NOT_FOUND)
            return Response({'message': 'Tour marked successfully'}, status=status.HTTP_201_CREATED)
        return Response({'message': 'Invalid data provided'}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        if request.query_params is not None:
            customer_id = request.query_params.get('customer_id', None)
            tour_id = request.query_params.get('tour_id', None)
            try:
                customer = es.get(index='customers', id=customer_id)
                tour = es.get(index='tours', id=tour_id)

                customer.marked_tours.remove(tour)
                customer.save()
                return Response({'message': 'Tour unmarked successfully'}, status=status.HTTP_204_NO_CONTENT)
            except (Customer.DoesNotExist, Tour.DoesNotExist):
                return Response({'message': 'Customer or Tour not found'}, status=status.HTTP_404_NOT_FOUND)
        return Response({'message': 'Invalid data provided'}, status=status.HTTP_400_BAD_REQUEST)


class CustomerBookingTourAPIView(APIView):
    def post(self, request):
        if request.query_params is not None:
            customer_id = request.query_params.get('customer_id', None)
            tour_id = request.query_params.get('tour_id', None)
            try:
                customer = es.get(index='customers', id=customer_id)
                tour = es.get(index='tours', id=tour_id)

                customer.booked_tours.add(tour)
                customer.save()
            except:
                return Response({'message': 'Customer or Tour not found'}, status=status.HTTP_404_NOT_FOUND)
            return Response({'message': 'Tour booked successfully'}, status=status.HTTP_201_CREATED)
        return Response({'message': 'Invalid data provided'}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        if request.query_params is not None:
            customer_id = request.query_params.get('customer_id', None)
            tour_id = request.query_params.get('tour_id', None)
            try:
                customer = es.get(index='customers', id=customer_id)
                tour = es.get(index='tours', id=tour_id)

                customer.booked_tours.remove(tour)
                customer.save()
                return Response({'message': 'Tour unbooked successfully'}, status=status.HTTP_204_NO_CONTENT)
            except (Customer.DoesNotExist, Tour.DoesNotExist):
                return Response({'message': 'Customer or Tour not found'}, status=status.HTTP_404_NOT_FOUND)
        return Response({'message': 'Invalid data provided'}, status=status.HTTP_400_BAD_REQUEST)


class CustomerMarkingTourAllAPIView(APIView):
    def get(self, request):
        my_data = request.data

        try:
            customer_id = my_data.query_params.get('customer_id', None)
            customer = es.get(index='customers', id=customer_id)
            marked_tours = customer['_source']['marked_tours']
            return Response(marked_tours, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class CustomerBookingTourAllAPIView(APIView):
    def get(self, request):
        my_data = request.data

        try:
            customer_id = my_data.query_params.get('customer_id', None)
            customer = es.get(index='customers', id=customer_id)
            booked_tours = customer['_source']['booked_tours']
            return Response(booked_tours, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)
