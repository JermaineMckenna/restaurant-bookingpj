from django.shortcuts import render, redirect
from .forms import BookingForm, ContactMessageForm
from .models import Booking, ContactMessage
from rest_framework import viewsets
from .serializers import BookingSerializer, ContactMessageSerializer

# Import the Google Calendar integration
from .google_calendar import create_event
from datetime import datetime, timedelta
import pytz


# 🏠 Homepage
def home(request):
    return render(request, 'homepageapp/home.html')


# 🍽️ Menu page
def menu(request):
    return render(request, 'homepageapp/menu.html')


# 📅 Booking form page with Google Calendar integration
def booking(request):
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save()  # Save booking to database

            # Prepare datetime for calendar
            tz = pytz.timezone('Europe/London')
            start_datetime = tz.localize(datetime.combine(booking.date, booking.time))
            end_datetime = start_datetime + timedelta(hours=2)  # Default slot length

            # Try to create a Google Calendar event safely
            try:
                event = create_event(
                    title=f"Booking: {booking.name}",
                    start_datetime=start_datetime,
                    end_datetime=end_datetime,
                    description=(
                        f"Name: {booking.name}\n"
                        f"Email: {booking.email}\n"
                        f"Phone: {booking.phone}\n"
                        f"Guests: {booking.guests}\n"
                        f"Special Requests: {booking.special_requests or 'N/A'}"
                    )
                )
                # Only show event link if calendar event was created successfully
                return render(
                    request,
                    'homepageapp/booking_success.html',
                    {'event_link': event.get('htmlLink') if event else None}
                )
            except Exception as e:
                print("⚠️ Google Calendar Error:", e)
                # Even if API fails, show success page for user
                return render(
                    request,
                    'homepageapp/booking_success.html',
                    {'event_link': None, 'error': 'Google Calendar event could not be created.'}
                )
    else:
        form = BookingForm()
    return render(request, 'homepageapp/booking.html', {'form': form})


# ✅ Booking success page
def booking_success(request):
    return render(request, 'homepageapp/booking_success.html')


# 🧱 Base template
def base(request):
    return render(request, 'homepageapp/base.html')


# 📩 Contact form page
def contact(request):
    if request.method == 'POST':
        form = ContactMessageForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('contact_success')
    else:
        form = ContactMessageForm()
    return render(request, 'homepageapp/contact.html', {'form': form})


# 📬 Contact success page
def contact_success(request):
    return render(request, 'homepageapp/contact_success.html')


# 🌐 API: Booking
class BookingViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.all().order_by('-created_at')
    serializer_class = BookingSerializer


# 🌐 API: Contact Messages
class ContactMessageViewSet(viewsets.ModelViewSet):
    queryset = ContactMessage.objects.all().order_by('-created_at')
    serializer_class = ContactMessageSerializer