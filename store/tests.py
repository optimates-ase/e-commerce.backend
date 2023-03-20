from django.http import HttpResponse
from django.test import TestCase
from .views import hello_word

# Create your tests here.

class HelloWorldTest(TestCase):
    def test_hello_world(self):
        self.assertEqual(HttpResponse("Hello world").content, hello_word("GET /store/hello/ HTTP/1.1").content)

