from django.shortcuts import render

def GetTQuotesData(request):
    return render(request, 'TQuotes.html')