from django.shortcuts import render

def GetQuotesDataFromTY(request):
    return render(request, 'quotes.html')