from django.contrib import admin

from .models import Customer, Device, RepairTicket

# Register your models here.

# Customer Admin
class CustomerAdmin(admin.ModelAdmin):
    list_display = ("full_name", "phone", "email", "created_at")
    search_fields = ("full_name", "phone", "email")
    ordering = ("-created_at",)

admin.site.register(Customer, CustomerAdmin)


# Device Admin
class DeviceAdmin(admin.ModelAdmin):
    list_display = (
        "brand",
        "model_name",
        "device_type",
        "customer",
        "imei_or_serial",
        "created_at",
        )

    list_filter = ("device_type",)

    search_fields = (
        "brand",
        "model_name",
        "imei_or_serial",
        "customer__full_name",
        "customer__phone",
    )

    ordering = ("-created_at",)


admin.site.register(Device, DeviceAdmin)

# Repair Ticket Admin
# @admin.register(RepairTicket)
class RepairTicketAdmin(admin.ModelAdmin):
    list_display = (
        "tracking_code",
        "device",
        "status",
        "assigned_technician",
        "expected_completion_date",
        "created_at",
    )

    list_filter = (
        "status",
        "assigned_technician",
        "created_at",
    )

    search_fields = (
        "tracking_code",
        "device__customer__full_name",
        "device__customer__phone",
        "device__brand",
        "device__model_name",
        "device__imei_or_serial",
    )

    readonly_fields = (
        "tracking_code",
        "created_at",
        "updated_at",
    )

    ordering = ("-created_at",)
admin.site.register(RepairTicket, RepairTicketAdmin)