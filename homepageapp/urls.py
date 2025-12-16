from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('menu/', views.menu, name='menu'),

    # Booking
    path('booking/', views.booking, name='booking'),
    path('booking-success/', views.booking_success, name='booking_success'),
    path('manage-booking/', views.manage_booking, name='manage_booking'),
    path('bookings/<str:reference_code>/', views.booking_detail, name='booking_detail'),
    path('bookings/<str:reference_code>/edit/', views.booking_update, name='booking_update'),
    path('bookings/<str:reference_code>/delete/', views.booking_delete, name='booking_delete'),

    # Contact messages
    path('contact/', views.contact, name='contact'),
    path('contact-success/', views.contact_success, name='contact_success'),

    # ✅ NEW: User CRUD for messages (no login)
    path('manage-message/', views.manage_message, name='manage_message'),
    path('messages/<str:reference_code>/', views.message_detail, name='message_detail'),
    path('messages/<str:reference_code>/edit/', views.message_update, name='message_update'),
    path('messages/<str:reference_code>/delete/', views.message_delete, name='message_delete'),
]