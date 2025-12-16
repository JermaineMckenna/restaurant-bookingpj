from django.contrib import admin
from .models import Booking, ContactMessage, Table, MenuItem


@admin.register(Table)
class TableAdmin(admin.ModelAdmin):
    list_display = ("table_number", "capacity")
    search_fields = ("table_number",)
    ordering = ("table_number",)


@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "price")
    list_filter = ("category",)
    search_fields = ("name",)
    ordering = ("category", "name")


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ("reference_code", "name", "email", "date", "time", "guests", "created_at")
    list_filter = ("date", "guests")
    search_fields = ("reference_code", "name", "email", "phone")
    ordering = ("-created_at",)
    readonly_fields = ("reference_code", "created_at")


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "created_at")
    search_fields = ("name", "email", "message")
    ordering = ("-created_at",)
    readonly_fields = ("created_at",)

