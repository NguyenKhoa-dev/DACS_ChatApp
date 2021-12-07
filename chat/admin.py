from django.contrib import admin
from .models import Room, Message, Information,RoomHistory
# Register your models here.
admin.site.register(Room)
admin.site.register(Message)
admin.site.register(Information)
admin.site.register(RoomHistory)