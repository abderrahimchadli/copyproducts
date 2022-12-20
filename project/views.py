from django.contrib import admin
from django.urls import include, path
from django.shortcuts import render


def error_404_view(request, exception):
       
    # we add the path to the the 404.html file
    # here. The name of our HTML file is 404.html
    return render(request, 'error-404.html')


def error_500_view(request, *args, **argv):
       
    # we add the path to the the 404.html file
    # here. The name of our HTML file is 404.html
    return render(request, 'error-500.html',status=500)


def error_403_view(request, exception):
       
    # we add the path to the the 404.html file
    # here. The name of our HTML file is 404.html
    return render(request, 'error-403.html')

