from rest_framework import serializers # type: ignore
from .models import Booking, ContactMessage


# 🧾 Booking Serializer (for Booking API)
class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = '__all__'


# 💌 Contact Message Serializer (for Contact API)
class ContactMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactMessage
        fields = '__all__'