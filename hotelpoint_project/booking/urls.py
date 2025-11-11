from django.urls import path
from .views import BookingCreateView, BookingListView, BookingDeleteView

urlpatterns = [
    path('new/', BookingCreateView.as_view(), name='booking_create'),
    path('list/', BookingListView.as_view(), name='booking_list'),
    path('<int:pk>/delete/', BookingDeleteView.as_view(), name='booking_delete'),
]