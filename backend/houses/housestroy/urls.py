from django.urls import path
from housestroy.views import *

urlpatterns = [
    path('', home_page, name='home_page'),
    path('catalog/', catalog, name='catalog'),
    path('catalog/<slug:slug>/', get_house, name='get_house'),
    path('api/houses/', HouseListView.as_view(), name='house-list')
]
