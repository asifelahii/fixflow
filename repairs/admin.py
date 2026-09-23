from django.contrib import admin

from .models import Customer

# Register your models here.

class CustomerAdmin(admin.ModelAdmin):
    list_display = ("full_name", "phone", "email", "created_at")
    search_fields = ("full_name", "phone", "email")
    ordering = ("-created_at",)

admin.site.register(Customer, CustomerAdmin)