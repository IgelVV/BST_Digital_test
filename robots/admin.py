from django.contrib import admin
from robots.models import Robot


@admin.register(Robot)
class RobotsAdmin(admin.ModelAdmin):
    ...
