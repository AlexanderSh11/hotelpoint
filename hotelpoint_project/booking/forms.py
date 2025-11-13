from django import forms
from .models import Booking
from clients.models import Client
from rooms.models import Room


class BookingForm(forms.ModelForm):
    first_name = forms.CharField(label='Имя', max_length=50)
    last_name = forms.CharField(label='Фамилия', max_length=50)
    middle_name = forms.CharField(label='Отчество', required=False, max_length=50)
    email = forms.EmailField(label='Email')
    phone = forms.CharField(label='Телефон', max_length=20)
    calculate = forms.BooleanField(
        required=False,
        widget=forms.HiddenInput(),
        initial=False
    )

    class Meta:
        model = Booking
        fields = ['room', 'check_in', 'check_out', 'has_child_bed']
        widgets = {
            'check_in': forms.DateInput(attrs={
                'type': 'date',
            }),
            'check_out': forms.DateInput(attrs={
                'type': 'date', 
            }),
        }

    def save(self, commit=True):
        data = self.cleaned_data
        client, _ = Client.objects.get_or_create(
            email=data['email'],
            defaults={
                'first_name': data['first_name'],
                'last_name': data['last_name'],
                'middle_name': data['middle_name'],
                'phone': data['phone'],
            }
        )
        booking = super().save(commit=False)
        booking.client = client
        if commit:
            booking.save()
        return booking