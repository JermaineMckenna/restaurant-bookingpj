from django import forms
from django.core.validators import RegexValidator
from django.utils import timezone
from datetime import datetime, time as time_obj

from .models import Booking, ContactMessage


# 🧾 Booking Form
class BookingForm(forms.ModelForm):
    phone = forms.CharField(
        max_length=20,
        validators=[
            RegexValidator(
                regex=r"^[0-9+\-\s()]{7,20}$",
                message="Enter a valid phone number (digits, spaces, +, -, parentheses)."
            )
        ],
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '+44 123 456 789'
        })
    )

    class Meta:
        model = Booking
        fields = ['name', 'email', 'phone', 'date', 'time', 'guests', 'special_requests']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Your Name'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'you@example.com'
            }),
            'date': forms.DateInput(attrs={
                'type': 'date',
                'class': 'form-control'
            }),
            'time': forms.TimeInput(attrs={
                'type': 'time',
                'class': 'form-control'
            }),
            'guests': forms.NumberInput(attrs={
                'min': 1,
                'class': 'form-control'
            }),
            'special_requests': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Any special requests...'
            }),
        }

    def clean_guests(self):
        guests = self.cleaned_data.get('guests')
        if guests and guests > 20:
            raise forms.ValidationError("We currently accept up to 20 guests per booking.")
        if guests and guests < 1:
            raise forms.ValidationError("Guests must be at least 1.")
        return guests

    def clean_date(self):
        booking_date = self.cleaned_data.get("date")
        if booking_date:
            today = timezone.localdate()
            if booking_date < today:
                raise forms.ValidationError("Please choose a date in the future.")
        return booking_date

    def clean(self):
        cleaned_data = super().clean()
        booking_date = cleaned_data.get("date")
        booking_time = cleaned_data.get("time")

        if booking_date and booking_time:
            opening = time_obj(11, 0)
            closing = time_obj(23, 0)

            if booking_time < opening or booking_time > closing:
                self.add_error("time", "Bookings must be between 11:00 and 23:00.")

            now = timezone.localtime()
            if booking_date == now.date():
                selected_dt = datetime.combine(booking_date, booking_time)
                selected_dt = timezone.make_aware(selected_dt, now.tzinfo)
                if selected_dt < now:
                    self.add_error("time", "Please choose a time later today (in the future).")

        return cleaned_data


# ✅ Find Booking Form (for managing bookings without login/accounts)
class FindBookingForm(forms.Form):
    reference_code = forms.CharField(
        max_length=12,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Booking reference (e.g. A1B2C3D4E5F6)'
        })
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Email used for booking'
        })
    )

    def clean_reference_code(self):
        return self.cleaned_data['reference_code'].strip().upper()


# 💌 Contact Message Form (create + update)
class ContactMessageForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'message']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Your Full Name'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'you@example.com'
            }),
            'message': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 5,
                'placeholder': 'Write your message here...'
            }),
        }

    def clean_message(self):
        message = self.cleaned_data.get('message', '')
        if len(message.strip()) < 10:
            raise forms.ValidationError("Please enter a bit more detail in your message.")
        return message


# ✅ NEW: Find Message Form (manage message without login)
class FindMessageForm(forms.Form):
    reference_code = forms.CharField(
        max_length=12,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Message reference (e.g. A1B2C3D4E5F6)'
        })
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Email used in the message'
        })
    )

    def clean_reference_code(self):
        return self.cleaned_data['reference_code'].strip().upper()

