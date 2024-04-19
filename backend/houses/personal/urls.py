from django.urls import path
from personal.views import personal_view

urlpatterns = [
    path('personal/', personal_view, name='personal_view'),
]
