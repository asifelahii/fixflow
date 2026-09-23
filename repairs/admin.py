from django.contrib import admin

from .models import (
    Customer,
    Device,
    RepairTicket,
    DeviceCondition,
    IntakePhoto,
    RepairStatusHistory,
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




# Repair Status History Admin
class RepairStatusHistoryAdmin(admin.ModelAdmin):
    list_display = (
        "ticket",
        "from_status",
        "to_status",
        "changed_by",
        "created_at",
    )

    list_filter = (
        "to_status",
        "created_at",
    )

    search_fields = (
        "ticket__tracking_code",
        "ticket__device__customer__full_name",
        "ticket__device__customer__phone",
    )

    readonly_fields = (
        "ticket",
        "from_status",
        "to_status",
        "changed_by",
        "customer_note",
        "created_at",
    )

    ordering = (
        "-created_at",
    )


admin.site.register(
    RepairStatusHistory,
    RepairStatusHistoryAdmin,
)




# Repair Status History Inline Admin
class RepairStatusHistoryInline(admin.TabularInline):
    model = RepairStatusHistory
    extra = 0

    fields = (
        "from_status",
        "to_status",
        "changed_by",
        "customer_note",
        "created_at",
    )

    readonly_fields = (
        "from_status",
        "to_status",
        "changed_by",
        "customer_note",
        "created_at",
    )

    can_delete = False

    def has_add_permission(
        self,
        request,
        obj=None,
    ):
        return False





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
        RepairStatusHistoryInline
    )

    ordering = (
        "-created_at",
    )

    def save_model(
    self,
    request,
    obj,
    form,
    change,
    ):
        if change and "status" in form.changed_data:
            previous_status = (
                RepairTicket.objects
                .only("status")
                .get(pk=obj.pk)
                .status
            )

            new_status = obj.status

            customer_note = ""
            if "customer_visible_note" in form.changed_data:
                customer_note = obj.customer_visible_note

            obj.status = previous_status

            super().save_model(
                request,
                obj,
                form,
                change,
            )

            obj.change_status(
                new_status=new_status,
                changed_by=request.user,
                customer_note=customer_note,
            )

            return

        super().save_model(
            request,
            obj,
            form,
            change,
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



