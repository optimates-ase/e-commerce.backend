from django.shortcuts import render
from django.http import HttpResponse


def hello_word(request):
    return HttpResponse("Hello world")
    