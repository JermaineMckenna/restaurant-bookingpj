from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.urls import reverse
from .forms import BookingForm, ContactMessageForm, FindBookingForm
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


# 📅 Booking form page with Google Calendar integration (uses PRG)
def booking(request):
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save()  # Save booking to database

            # Prepare datetime for calendar
            tz = pytz.timezone('Europe/London')
            start_datetime = tz.localize(datetime.combine(booking.date, booking.time))
            end_datetime = start_datetime + timedelta(hours=2)  # Default slot length

            # google calendar event
            event_link = None
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
                if isinstance(event, dict):
                    event_link = event.get('htmlLink')
            except Exception as e:
                # Log server-side; keep UX clean
                print("⚠️ Google Calendar Error:", e)
                messages.warning(
                    request,
                    "Your booking was saved, but we couldn’t create a calendar entry this time."
                )

            # Store info in session for the success page and redirect
            request.session['event_link'] = event_link
            request.session['last_booking_name'] = booking.name
            request.session['last_booking_when'] = f"{booking.date} at {booking.time}"

            # ✅ NEW: Store booking reference so user can manage it later (CRUD)
            request.session['last_booking_ref'] = booking.reference_code

            return redirect('booking_success')
        # If invalid, fall through and re-render with errors
    else:
        form = BookingForm()

    return render(request, 'homepageapp/booking.html', {'form': form})


# ✅ Booking success page (pulls info from session; safe if nothing there)
def booking_success(request):
    context = {
        'event_link': request.session.pop('event_link', None),
        'booking_name': request.session.pop('last_booking_name', None),
        'booking_when': request.session.pop('last_booking_when', None),
        # ✅ NEW
        'booking_ref': request.session.pop('last_booking_ref', None),
    }
    return render(request, 'homepageapp/booking_success.html', context)


# ✅ NEW: Manage booking (enter reference + email)
def manage_booking(request):
    if request.method == "POST":
        form = FindBookingForm(request.POST)
        if form.is_valid():
            ref = form.cleaned_data["reference_code"]
            email = form.cleaned_data["email"]

            booking_obj = Booking.objects.filter(reference_code=ref, email=email).first()
            if not booking_obj:
                messages.error(request, "Booking not found. Please check your reference code and email.")
                return render(request, "homepageapp/manage_booking.html", {"form": form})

            return redirect("booking_detail", reference_code=booking_obj.reference_code)
    else:
        form = FindBookingForm()

    return render(request, "homepageapp/manage_booking.html", {"form": form})


# ✅ NEW: READ booking
def booking_detail(request, reference_code):
    booking_obj = get_object_or_404(Booking, reference_code=reference_code)
    return render(request, "homepageapp/booking_detail.html", {"booking": booking_obj})


# ✅ NEW: UPDATE booking
def booking_update(request, reference_code):
    booking_obj = get_object_or_404(Booking, reference_code=reference_code)

    if request.method == "POST":
        form = BookingForm(request.POST, instance=booking_obj)
        if form.is_valid():
            form.save()
            messages.success(request, "Booking updated successfully.")
            return redirect("booking_detail", reference_code=booking_obj.reference_code)
    else:
        form = BookingForm(instance=booking_obj)

    return render(request, "homepageapp/booking_update.html", {"form": form, "booking": booking_obj})


# ✅ NEW: DELETE booking
def booking_delete(request, reference_code):
    booking_obj = get_object_or_404(Booking, reference_code=reference_code)

    if request.method == "POST":
        booking_obj.delete()
        messages.success(request, "Booking cancelled successfully.")
        return redirect("manage_booking")

    return render(request, "homepageapp/booking_confirm_delete.html", {"booking": booking_obj})


# 🧱 Base template
def base(request):
    return render(request, 'homepageapp/base.html')


# 📩 Contact form page (PRG with messages)
def contact(request):
    if request.method == 'POST':
        form = ContactMessageForm(request.POST)
        if form.is_valid():
            try:
                form.save()
            except Exception as e:
                print("[Contact] Save error:", e)
                messages.error(request, "Sorry, something went wrong saving your message.")
                return render(request, 'homepageapp/contact.html', {'form': form})

            messages.success(request, "Thanks! Your message has been sent.")
            return redirect('contact_success')
        # invalid: fall through to re-render
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