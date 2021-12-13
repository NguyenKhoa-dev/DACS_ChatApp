import json
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async
# from channels.db import database_sync_to_async
from .models import Message, Room, Information, RoomHistory
from django.contrib.auth.models import User

class ChatConsumer(AsyncWebsocketConsumer):
    room_id = 0
    username = ""
    
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_id']
        self.room_group_name = f'chat_{self.room_name}'
        self.user = self.scope['user']

        # Join room
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room
        # print("hello")
        print(self.username)
        print(self.room_id)
        # # infors = await self.get_users(self.room_id,self.username,False)
        rhs = await self.get_users(self.room_id,self.username,False)
        for rh in rhs:
            #f'user_{info.user.id}'
            await self.channel_layer.group_send(
                self.room_group_name, 
                {
                    'type':'user_status',
                    'user_id':rh.user.id,
                    'status':rh.status
                }
            )
        # self.set_status()
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from web socket
    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data.get('message')
        self.username = data.get('username')
        self.room_id = data.get('room_id')
        type_set = data.get('type_set')
        status = data.get('status')
        print(self.username)
        print(self.room_id)
        
        if type_set=="CHAT":
            date = await self.save_message(self.username, self.room_id, message)
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'message': message,
                    'username': self.username,
                    'date': date
                }
            )
        elif type_set=="USERS":
            rhs = await self.get_users(self.room_id,self.username,True)
            for rh in rhs:
                #f'user_{info.user.id}'
                await self.channel_layer.group_send(
                    self.room_group_name, 
                    {
                        'type':'user_status',
                        'user_id':rh.user.id,
                        'status':rh.status
                    }
                )
    
    async def user_status(self,event):
        user_id = event['user_id']
        status = event['status']
        str = "OFFLINE"
        if status==True: str = "ONLINE"
        await self.send(text_data=json.dumps({
            'type_set':'USERS',
            'user_id':user_id,
            'status':str
        }))
    
    # Receive message from room group
    async def chat_message(self, event):
        message = event['message']
        username = event['username']
        date = event['date']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'type_set':'CHAT',
            'message': message,
            'username': username,
            'date': date
        }))

    @sync_to_async
    def save_message(self, username, room_id, message):
        room = Room.objects.filter(id=room_id).first()
        user = User.objects.filter(username=username).first()
        message = Message.objects.create(user=user, room=room, content=message)
        return message.date_added.strftime("%d/%m/%Y %H:%M")
    
    @sync_to_async
    def get_users(self,room_id,username,status):
        user = User.objects.get(username=username)
        room = Room.objects.get(id=room_id)
        RoomHistory.objects.filter(room=room,user=user).update(status=status)
        rhs = RoomHistory.objects.filter(room=room)
        return rhs