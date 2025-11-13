from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, ListView, DeleteView
from rooms.models import Room
from .models import Booking
from .forms import BookingForm
from clients.models import Client


class BookingListView(LoginRequiredMixin, ListView):
    model = Booking
    template_name = 'booking/booking_list.html'
    context_object_name = 'bookings'
    ordering = ['-check_in']

    def get_queryset(self):
        queryset = super().get_queryset()
        client_id = self.kwargs.get('client_id')
        room_id = self.kwargs.get('room_id')
        if client_id:
            queryset = queryset.filter(client_id=client_id)
        if room_id:
            queryset = queryset.filter(room_id=room_id)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        client_id = self.kwargs.get('client_id')
        room_id = self.kwargs.get('room_id')
        if client_id:
            try:
                context['current_client'] = Client.objects.get(id=client_id)
            except (Client.DoesNotExist, ValueError):
                context['current_client'] = None
        if room_id:
            try:
                context['current_room'] = Room.objects.get(id=room_id)
            except (Room.DoesNotExist, ValueError):
                context['current_room'] = None
        return context


class BookingCreateView(LoginRequiredMixin, CreateView):
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
    
    def post(self, request, *args, **kwargs):
        self.object = None
        form = self.get_form()
        
        if 'calculate' in request.POST:
            if form.is_valid():
                booking = form.save(commit=False)
                calculated_price = booking.calculate_total_price()
                duration = booking.duration
                
                return self.render_to_response(
                    self.get_context_data(
                        form=form,
                        show_calculation=True,
                        calculated_price=calculated_price,
                        duration=duration
                    )
                )
            else:
                return self.form_invalid(form)
        
        elif 'book' in request.POST:
            if form.is_valid():
                return self.form_valid(form)
            else:
                return self.form_invalid(form)
        
        return self.form_invalid(form)

    def form_valid(self, form):
        booking = form.save(commit=False)
        booking.total_price = booking.calculate_total_price()
        
        try:
            booking.full_clean()
        except Exception as e:
            form.add_error(None, e)
            return self.form_invalid(form)
        
        booking.save()
        return super().form_valid(form)


class BookingDeleteView(LoginRequiredMixin, DeleteView):
    model = Booking
    template_name = 'booking/booking_delete.html'
    success_url = reverse_lazy('booking_list')