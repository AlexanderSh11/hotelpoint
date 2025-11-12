from django.urls import path
from .views import ClientListView

urlpatterns = [
    path('list/', ClientListView.as_view(), name='client_list'),
]