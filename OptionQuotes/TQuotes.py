from django.shortcuts import render

def GetTQuotesData(request):
    print(request.POST.get('value'))
    return render(request, 'TQuotes.html')