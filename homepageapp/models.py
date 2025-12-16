from django.db import models
from django.contrib.auth.models import User  # ✅ Built-in Django user model
import uuid


# 🍽️ Table Model
# Represents each physical table that can be booked by customers.
class Table(models.Model):
    table_number = models.IntegerField(unique=True)
    capacity = models.PositiveIntegerField()

    def __str__(self):
        return f"Table {self.table_number} (Seats {self.capacity})"


# 🧾 Booking Model
# Stores all restaurant bookings linked to both users and tables.
class Booking(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="bookings",
        null=True,
        blank=True,  # allows guest bookings if not logged in
    )
    table = models.ForeignKey(
        Table,
        on_delete=models.CASCADE,
        related_name="bookings",
        null=True,
        blank=True,  # allows bookings without assigning a specific table
    )

    # ✅ Reference code to allow users to manage bookings without accounts/login
    reference_code = models.CharField(max_length=20, unique=True, editable=False)

    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    date = models.DateField()
    time = models.TimeField()
    guests = models.PositiveIntegerField()
    special_requests = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.reference_code:
            # 12-char uppercase reference, e.g. "A1B2C3D4E5F6"
            self.reference_code = uuid.uuid4().hex[:12].upper()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} - {self.date} at {self.time}"


# 🍴 Menu Item Model
# Optional menu model for displaying or managing food items.
class MenuItem(models.Model):
    CATEGORY_CHOICES = [
        ("starter", "Starter"),
        ("main", "Main"),
        ("dessert", "Dessert"),
        ("drink", "Drink"),
    ]

    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)

    def __str__(self):
        return f"{self.name} (£{self.price})"


# 💬 Contact Message Model
# Stores customer contact form submissions.
class ContactMessage(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,  # user optional
        related_name="contact_messages",
    )

    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.reference_code:
            self.reference_code = uuid.uuid4().hex[:12].upper()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Message from {self.name} ({self.email})"



