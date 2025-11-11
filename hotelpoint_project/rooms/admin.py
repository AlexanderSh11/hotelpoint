from django.contrib import admin
from .models import RoomCategory, Room, RoomPrice

admin.site.register(RoomCategory)
admin.site.register(Room)
admin.site.register(RoomPrice)