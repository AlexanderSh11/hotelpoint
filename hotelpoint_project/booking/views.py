from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, DeleteView
from .models import Booking
from .forms import BookingForm


class BookingListView(ListView):
    model = Booking
    template_name = 'booking/booking_list.html'
    context_object_name = 'bookings'
    ordering = ['-check_in']


class BookingCreateView(CreateView):
    model = Booking
    form_class = BookingForm
    template_name = 'booking/booking_form.html'
    success_url = reverse_lazy('booking_list')

    def get_initial(self):
        initial = super().get_initial()
        room_id = self.request.GET.get('room')
        if room_id:
            initial['room'] = room_id
        return initial


class BookingDeleteView(DeleteView):
    model = Booking
    template_name = 'booking/booking_delete.html'
    success_url = reverse_lazy('booking_list')