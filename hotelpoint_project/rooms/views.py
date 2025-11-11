from django.views.generic import ListView, DetailView
from .models import Room


class RoomListView(ListView):
    model = Room
    context_object_name = 'rooms'
    queryset = Room.objects.select_related('category').all()


class RoomDetailView(DetailView):
    model = Room
    context_object_name = 'room'
