from django.http import HttpResponse
from django.shortcuts import render


def hello_world(request):
    return HttpResponse("Hello, Django World!")

def greet(request):
    return render(request, "hello/greet.html", {"name": "Student"})