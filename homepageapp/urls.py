from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("menu/", views.menu, name="menu"),

    # Booking (Full user CRUD - no login)
    path("booking/", views.booking, name="booking"),
    path("booking-success/", views.booking_success, name="booking_success"),
    path("manage-booking/", views.manage_booking, name="manage_booking"),
    path("bookings/<str:reference_code>/", views.booking_detail, name="booking_detail"),
    path("bookings/<str:reference_code>/edit/", views.booking_update, name="booking_update"),
    path("bookings/<str:reference_code>/delete/", views.booking_delete, name="booking_delete"),

    # Contact messages (Create only for users; staff can manage in admin)
    path("contact/", views.contact, name="contact"),
    path("contact-success/", views.contact_success, name="contact_success"),
]