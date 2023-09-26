from django.contrib import admin
from customers.models import Customer


@admin.register(Customer)
class RobotAdmin(admin.ModelAdmin):
    list_display = ("pk", "email")
