import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.contrib.auth import get_user_model
from .models import Chat, Message

User = get_user_model()

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.chat_id = self.scope['url_route']['kwargs']['chat_id']
        self.chat_group_name = f'chat_{self.chat_id}'

        if not await self.user_in_chat():
            await self.close()
            return

        await self.channel_layer.group_add(
            self.chat_group_name,
            self.channel_name
        )

        await self.accept()

        
        await self.mark_messages_read()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.chat_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        data = json.loads(text_data)
        text = data.get('text', '').strip()
        action = data.get('action', 'send')  

        if action == 'mark_read':
            await self.mark_messages_read()
            return

        if not text:
            return

        user = self.scope['user']

        if not await self.user_in_chat():
            await self.close()
            return

        await self.save_message(user.id, self.chat_id, text)

        await self.channel_layer.group_send(
            self.chat_group_name,
            {
                'type': 'chat_message',
                'text': text,
                'user_id': user.id,
                'username': user.get_full_name(),
            }
        )

    async def chat_message(self, event):
        await self.send(text_data=json.dumps({
            'text': event['text'],
            'user_id': event['user_id'],
            'username': event['username'],
        }))

    @database_sync_to_async
    def save_message(self, user_id, chat_id, text):
        user = User.objects.get(id=user_id)
        chat = Chat.objects.get(id=chat_id)
        return Message.objects.create(user=user, chat=chat, text=text)

    @database_sync_to_async
    def user_in_chat(self):
        user = self.scope['user']
        return Chat.objects.filter(
            id=self.chat_id,
            teacher=user
        ).exists() or Chat.objects.filter(
            id=self.chat_id,
            student=user
        ).exists()

    @database_sync_to_async
    def mark_messages_read(self):
        user = self.scope['user']
        
        Message.objects.filter(
            chat_id=self.chat_id,
            is_read=False
        ).exclude(user=user).update(is_read=True)
