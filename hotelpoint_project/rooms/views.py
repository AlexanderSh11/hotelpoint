from django.views.generic import ListView, DetailView
from booking.models import Booking
from .models import Room
from django.db.models import Q
from django.utils.dateparse import parse_date


class RoomListView(ListView):
    model = Room
    context_object_name = 'rooms'

    def get_queryset(self):
        queryset = Room.objects.all()
        check_in = self.request.GET.get('check_in')
        check_out = self.request.GET.get('check_out')

        if check_in and check_out:
            check_in_date = parse_date(check_in)
            check_out_date = parse_date(check_out)

            # Находим все брони, которые пересекаются с выбранным периодом
            booked_rooms = Booking.objects.filter(
                Q(check_in__lt=check_out_date) & Q(check_out__gt=check_in_date)
            ).values_list('room_id', flat=True)

            # Исключаем занятые номера
            queryset = queryset.exclude(id__in=booked_rooms)

        return queryset


class RoomDetailView(DetailView):
    model = Room
    context_object_name = 'room'
