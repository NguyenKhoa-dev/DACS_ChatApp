import json

from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async

from .models import Message,Room
from django.contrib.auth.models import User

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_id']
        self.room_group_name = 'chat_%s' % self.room_name

        # Join room
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()
    
    async def disconnect(self, close_code):
        # Leave room
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
    
    # Receive message from web socket
    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data['message']
        username = data['username']
        room_id = data['room_id']

        date = await self.save_message(username, room_id, message)

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'username': username,
                'date':date
            }
        )
    
    # Receive message from room group
    async def chat_message(self, event):
        message = event['message']
        username = event['username']
        date = event['date']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message,
            'username': username,
            'date':date
        }))

    @sync_to_async
    def save_message(self, username, room_id, message):
        room = Room.objects.filter(id=room_id).first()
        user = User.objects.filter(username=username).first()
        message = Message.objects.create(user=user, room=room, content=message)
        return message.date_added.strftime("%d/%m/%Y %H:%M")