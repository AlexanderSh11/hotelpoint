from django import forms
from .models import Booking
from clients.models import Client
from rooms.models import Room


class BookingForm(forms.ModelForm):
    name = forms.CharField(label='Полное имя', max_length=150)
    email = forms.EmailField(label='Email')
    phone = forms.CharField(label='Телефон', max_length=20)

    class Meta:
        model = Booking
        fields = ['room', 'check_in', 'check_out', 'has_child_bed']
        widgets = {
            'check_in': forms.DateInput(attrs={'type': 'date'}),
            'check_out': forms.DateInput(attrs={'type': 'date'}),
        }

    def save(self, commit=True):
        data = self.cleaned_data
        client, _ = Client.objects.get_or_create(
            email=data['email'],
            defaults={
                'name': data['name'],
                'phone': data['phone'],
            }
        )
        booking = super().save(commit=False)
        booking.client = client
        if commit:
            booking.save()
        return booking