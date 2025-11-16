from django.contrib import admin
from .models import Booking, ContactMessage, Table, MenuItem

admin.site.register(Table)
admin.site.register(MenuItem)
admin.site.register(Booking)
admin.site.register(ContactMessage)
