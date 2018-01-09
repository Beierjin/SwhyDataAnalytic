from django.shortcuts import render
from  django.db import connection

def test(request):
    cursor = connection.cursor
    print(cursor)

# Create your views here.
