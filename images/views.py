from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import render
from rest_framework.parsers import MultiPartParser, FormParser

import boto3

from .models import Image

# Create your views here.
class ImageAPIView(APIView):
    def get(self, request, format=None):
        name = request.query_params.get('name', None)

        s3 = boto3.client(
            's3',
            endpoint_url='http://localhost:4566',
            region_name='us-east-1'
        )
        
        bucket_name = 'optimates-images'
        expires_in_seconds = 3600

        presigned_url = s3.generate_presigned_url(
            ClientMethod='get_object',
            Params={
                'Bucket': bucket_name,
                'Key': name
            },
            ExpiresIn=expires_in_seconds
        )

        return Response(presigned_url,status=status.HTTP_200_OK)
    
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request, format=None):
        file_obj = request.FILES['file']

        s3 = boto3.client(
            's3',
            endpoint_url='http://localhost:4566',
            region_name='us-east-1'
        )

        bucket_name = 'optimates-images'
        key = file_obj.name

        try:
            s3.upload_fileobj(file_obj, bucket_name, key)
            return Response("Image uploaded successfully.", status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response(str(e), status=status.HTTP_500_INTERNAL_SERVER_ERROR)