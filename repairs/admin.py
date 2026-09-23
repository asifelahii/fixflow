from django.contrib import admin

from .models import Customer, Device

# Register your models here.

class CustomerAdmin(admin.ModelAdmin):
    list_display = ("full_name", "phone", "email", "created_at")
    search_fields = ("full_name", "phone", "email")
    ordering = ("-created_at",)

admin.site.register(Customer, CustomerAdmin)

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