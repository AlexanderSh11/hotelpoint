from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, DeleteView
from .models import Booking
from .forms import BookingForm
from .models import Client


class BookingListView(ListView):
    model = Booking
    template_name = 'booking/booking_list.html'
    context_object_name = 'bookings'
    ordering = ['-check_in']

    def get_queryset(self):
        queryset = super().get_queryset()
        client_id = self.kwargs.get('client_id')
        if client_id:
            queryset = queryset.filter(client_id=client_id)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        client_id = self.kwargs.get('client_id')
        if client_id:
            try:
                context['current_client'] = Client.objects.get(id=client_id)
            except (Client.DoesNotExist, ValueError):
                context['current_client'] = None
        return context


class BookingCreateView(CreateView):
    model = Booking
    form_class = BookingForm
    template_name = 'booking/booking_form.html'
    success_url = reverse_lazy('booking_list')

    def get_initial(self):
        initial = super().get_initial()
        room_id = self.kwargs.get('room_id')
        if room_id:
            initial['room'] = room_id
        return initial


class BookingDeleteView(DeleteView):
    model = Booking
    template_name = 'booking/booking_delete.html'
    success_url = reverse_lazy('booking_list')