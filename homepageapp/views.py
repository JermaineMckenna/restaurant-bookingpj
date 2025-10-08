from django.shortcuts import render, redirect
from .forms import BookingForm, ContactMessageForm
from .models import Booking, ContactMessage
from rest_framework import viewsets
from .serializers import BookingSerializer, ContactMessageSerializer

# Import the Google Calendar integration
from .google_calendar import add_booking_event


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

            # Create Google Calendar event
            event_link = add_booking_event(
                name=booking.name,
                email=booking.email,
                phone=booking.phone,
                date=booking.date,
                time=booking.time,
                guests=booking.guests,
                special_requests=booking.special_requests
            )

            # ✅ Pass the event link to the success page
            return render(request, 'homepageapp/booking_success.html', {'event_link': event_link})
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
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer


# 🌐 API: Contact Messages
class ContactMessageViewSet(viewsets.ModelViewSet):
    queryset = ContactMessage.objects.all()
    serializer_class = ContactMessageSerializer