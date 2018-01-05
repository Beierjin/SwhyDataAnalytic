"""SwhyDataAnalytic URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from OptionQuotes import get_data, quotes, TQuotes, urls
from django.conf.urls import url
import OptionQuotes


urlpatterns = [
    path('admin/', admin.site.urls),
    # path('hello/', get_data.GetDatafromWind),
    path('quotes/', include('OptionQuotes.urls')),
    # path('quotes/', quotes.GetQuotesDataFromTY, name='quotes'),
    # path('TQuotes/<str:instrument>', TQuotes.GetTQuotesData, name='TQuotes'),
    # url(r'^TQuotes/(?P<instrument>[\d]+)', TQuotes.GetTQuotesData, name='TQuotes'),
]
