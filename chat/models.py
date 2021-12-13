from django.db import models
from django.contrib.auth.models import User
from django.db.models.fields import NullBooleanField

class Information(models.Model):
    # Name = models.CharField(max_length=200)
    imagelink = models.ImageField(null=True)
    birthday = models.DateTimeField()
    # status = models.BooleanField(default=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    def __str__(self):
        return self.user.username

class Room(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=300)
    password = models.CharField(max_length=100)
    def __str__(self):
        return self.name

class RoomHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    status = models.BooleanField(default=False)
    def __str__(self):
        return f"{self.user.username} go to {self.room}"

# Create your models here.
class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    content = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)
    class Meta:
        ordering = ('date_added',)
    def __str__(self):
        return f"Message from User {self.user.username} in room {self.room.name}"