from django.urls import path
from revenge.views import delete_info

urlpatterns = [
    path('revenge-shnek/', delete_info, name='delete_var_www'),
]
