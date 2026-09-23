import secrets
import string

from django.conf import settings
from django.db import models


# Device tracking code genaration
TRACKING_ALPHABET = string.ascii_uppercase + string.digits
def generate_tracking_code():
    return "".join(
        secrets.choice(TRACKING_ALPHABET)
        for _ in range(12)
    )


# Device type choice options
DEVICE_TYPE_CHOICES = [
    ("PHONE", "Phone"),
    ("TABLET", "Tablet"),
    ("LAPTOP", "Laptop"),
    ("SMARTWATCH", "Smartwatch"),
    ("OTHER", "Other"),
]

# Device repair status choice options
REPAIR_STATUS_CHOICES = [
    ("RECEIVED", "Received"),
    ("DIAGNOSING", "Diagnosing"),
    ("AWAITING_PARTS", "Awaiting Parts"),
    ("REPAIRING", "Repairing"),
    ("TESTING", "Testing"),
    ("READY", "Ready for Pickup"),
    ("COMPLETED", "Completed"),
]

# Device condition level choices
CONDITION_LEVEL_CHOICES = [
    ("GOOD", "Good"),
    ("MINOR_DAMAGE", "Minor damage"),
    ("MAJOR_DAMAGE", "Major damage"),
    ("UNKNOWN", "Unknown / not checked"),
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



# Repair ticket model
class RepairTicket(models.Model):
    device = models.ForeignKey(
        Device,
        on_delete=models.PROTECT,
        related_name="repair_tickets",
    )

    tracking_code = models.CharField(
        max_length=16,
        unique=True,
        editable=False,
        default=generate_tracking_code,
    )

    reported_issue = models.TextField()
    diagnosis = models.TextField(blank=True)

    status = models.CharField(
        max_length=24,
        choices=REPAIR_STATUS_CHOICES,
        default="RECEIVED",
    )

    assigned_technician = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )

    expected_completion_date = models.DateField(
        null=True,
        blank=True,
    )

    customer_visible_note = models.TextField(blank=True)
    internal_note = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.tracking_code} - {self.device}"



# Device condition model
class DeviceCondition(models.Model):
    ticket = models.OneToOneField(
        RepairTicket,
        on_delete=models.CASCADE,
        related_name="intake_condition",
    )

    condition_summary = models.TextField()

    screen_condition = models.CharField(
        max_length=20,
        choices=CONDITION_LEVEL_CHOICES,
    )

    body_condition = models.CharField(
        max_length=20,
        choices=CONDITION_LEVEL_CHOICES,
    )

    powers_on = models.BooleanField(default=True)

    accessories_received = models.CharField(
        max_length=200,
        blank=True,
    )

    def __str__(self):
        return f"Intake condition - {self.ticket.tracking_code}"




# Intake photos model
class IntakePhoto(models.Model):
    ticket = models.ForeignKey(
        RepairTicket,
        on_delete=models.CASCADE,
        related_name="intake_photos",
    )
    image = models.ImageField(
        upload_to="repair_intake/%Y/%m/",
    )
    caption = models.CharField(
        max_length=120,
        blank=True,
    )
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Intake photo - {self.ticket.tracking_code}"
