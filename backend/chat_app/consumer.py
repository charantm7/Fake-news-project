# chat/consumers.py
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from django.contrib.auth.models import User
from .models import ChatMessage
from asgiref.sync import sync_to_async
from chat_app.views import analyze_message_with_mistral
import requests


OPENROUTER_API_KEY = "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" # our password
OPENROUTER_API_URL = "https://openrouter.ai/api/v1/chat/completions"

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.chat_name = self.scope['url_route']['kwargs']['chat_name']
        user1 = self.scope['user'].username 
        user2 = self.chat_name
        self.room_group_name = f"chat_{''.join(sorted([user1, user2]))}"

        # Join room group
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json.get('message')
        sender = self.scope['user']
        receiver_username = text_data_json.get('receiver')

        if receiver_username:
            receiver = await self.get_receiver_user(receiver_username)
        else:
            receiver = None

        if message:
            # Save the message to the database
            await self.save_message(sender, receiver, message)

            # Send the message to the room group
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'sender': sender.username,
                    'receiver': receiver.username if receiver else None,
                    'message': message,
                }
            )

        if text_data_json.get('type') == 'ai_analysis':
            ai_response = await self.analyze_message_with_mistral(text_data_json['content'])

            # Send the AI response to the room group
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'ai_response',
                    'sender': 'AI',
                    'content': f"AI: {ai_response}",
                }
            )

    async def chat_message(self, event):
        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'type': 'message',
            'sender': event['sender'],
            'receiver': event['receiver'],
            'message': event['message'],
        }))

    async def ai_response(self, event):
        # Send AI response to WebSocket
        await self.send(text_data=json.dumps({
            'type': 'ai_response',
            'sender': event['sender'],
            'content': event['content'],
        }))
    @sync_to_async
    def save_message(self, sender, receiver, message):
        ChatMessage.objects.create(sender=sender, receiver=receiver, content=message)

    @sync_to_async
    def get_receiver_user(self, username):
        return User.objects.get(username=self.chat_name)

    @sync_to_async
    def analyze_message_with_mistral(self, message):
        headers = {
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
            "Content-Type": "application/json",
            "HTTP-Referer": "http://localhost:8000",
            "X-Title": "Fake News Detector",
        }
        payload = {
            "model": "mistralai/mistral-7b-instruct:free",
            "messages": [{"role": "user", "content": f"Analyze this message for fake news: '{message}'."}],
        }
        try:
            response = requests.post(OPENROUTER_API_URL, headers=headers, json=payload)
            if response.status_code == 200:
                return response.json()["choices"][0]["message"]["content"]
            return f"Error: {response.status_code} - {response.text}"
        except Exception as e:
            return f"Error analyzing message: {str(e)}"