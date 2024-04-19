from django.urls import path
from application.views import ApplicationCreateView, Cost_ApplicationCreateView

urlpatterns = [

    path('api/application/create/', ApplicationCreateView.as_view(), name='create-application'),
    path('api/cost-application/create', Cost_ApplicationCreateView.as_view(), name='create-cost-application')

]
