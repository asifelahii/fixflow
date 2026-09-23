from django.db import models


# Device type choice options
DEVICE_TYPE_CHOICES = [
    ("PHONE", "Phone"),
    ("TABLET", "Tablet"),
    ("LAPTOP", "Laptop"),
    ("SMARTWATCH", "Smartwatch"),
    ("OTHER", "Other"),
]

# Customer model class
class Customer(models.Model):
    full_name = models.CharField(max_length=120)
    phone = models.CharField(max_length=20, unique=True)
    email = models.EmailField(blank=True)
    address = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.full_name} - {self.phone}"

# Device model class
class Device(models.Model):
    customer = models.ForeignKey(
        Customer,
        on_delete=models.PROTECT,
        related_name="devices",
    )
    device_type = models.CharField(
        max_length=20,
        choices=DEVICE_TYPE_CHOICES,
    )
    brand = models.CharField(max_length=80)
    model_name = models.CharField(max_length=120)
    color = models.CharField(max_length=50, blank=True)
    imei_or_serial = models.CharField(max_length=100, blank=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.brand} {self.model_name} - {self.customer.full_name}"