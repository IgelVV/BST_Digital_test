from django.contrib import admin
from orders.models import Order


@admin.register(Order)
class RobotAdmin(admin.ModelAdmin):
    ...
