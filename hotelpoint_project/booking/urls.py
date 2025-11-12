from django.urls import path
from .views import BookingCreateView, BookingListView, BookingDeleteView

urlpatterns = [
    path('new/', BookingCreateView.as_view(), name='booking_create'),
    path('new/room/<int:room_id>/', BookingCreateView.as_view(), name='booking_create_with_room'),
    path('list/', BookingListView.as_view(), name='booking_list'),
    path('list/client/<int:client_id>/', BookingListView.as_view(), name='booking_list_by_client'),
    path('<int:pk>/delete/', BookingDeleteView.as_view(), name='booking_delete'),
]