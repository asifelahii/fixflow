from django.contrib import admin

from .models import (
    Customer,
    Device,
    RepairTicket,
    DeviceCondition,
    IntakePhoto,
)

# Register your models here.

# Customer Admin
class CustomerAdmin(admin.ModelAdmin):
    list_display = (
        "full_name",
        "phone",
        "email",
        "created_at",
    )

    search_fields = (
        "full_name",
        "phone",
        "email",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
    )

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

    list_filter = (
        "device_type",
    )

    search_fields = (
        "brand",
        "model_name",
        "imei_or_serial",
        "customer__full_name",
        "customer__phone",
    )

    readonly_fields = (
        "created_at",
    )

    ordering = ("-created_at",)
admin.site.register(Device, DeviceAdmin)



# Intake Photo Inline Admin
class IntakePhotoInline(admin.TabularInline):
    model = IntakePhoto
    extra = 1
    fields = ("image", "caption")



# Repair Ticket Admin
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

    inlines = (
        IntakePhotoInline,
    )

    ordering = (
        "-created_at",
    )
admin.site.register(RepairTicket, RepairTicketAdmin)


# Device Condition Admin
class DeviceConditionAdmin(admin.ModelAdmin):
    list_display = (
        "ticket",
        "screen_condition",
        "body_condition",
        "powers_on",
    )

    list_filter = (
        "screen_condition",
        "body_condition",
        "powers_on",
    )

    search_fields = (
        "ticket__tracking_code",
        "ticket__device__customer__full_name",
        "ticket__device__customer__phone",
    )
admin.site.register(DeviceCondition, DeviceConditionAdmin)



# Intake Photo Admin
class IntakePhotoAdmin(admin.ModelAdmin):
    list_display = (
        "ticket",
        "caption",
        "uploaded_at",
    )

    search_fields = (
        "ticket__tracking_code",
        "ticket__device__customer__full_name",
        "ticket__device__customer__phone",
        "caption",
    )

    readonly_fields = (
        "uploaded_at",
    )

    ordering = (
        "-uploaded_at",
    )
admin.site.register(IntakePhoto, IntakePhotoAdmin)



