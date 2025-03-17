import json
import os
from channels.generic.websocket import AsyncWebsocketConsumer
from django.contrib.auth.models import User
from .models import ChatMessage
from asgiref.sync import sync_to_async
from datetime import datetime
import aiohttp

#5ZppSTNxyZcQqCuA5qWH2SZwHFI0gRcg
# Load API key from environment variables
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
        
        receiver = await self.get_receiver_user(self.chat_name)
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

            await self.save_message(sender, receiver, ai_response)  

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
        ChatMessage.objects.create(sender=sender, receiver=receiver, content=message, timestamp=datetime.now())

    @sync_to_async
    def get_receiver_user(self, username):
        try:
            return User.objects.get(username=self.chat_name)
        except User.DoesNotExist:
            return None
        

    

    async def analyze_message_with_mistral(self, message):
        headers = {
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
            "Content-Type": "application/json",
            "HTTP-Referer": "http://localhost:8000",
            "X-Title": "Fake News Detector",
        }
        payload = {
        "model": "mistralai/mistral-7b-instruct:free",
        "messages": [
            {
                "role": "user",
                "content": f"""
                    Analyze the following message for fake news: "{message}".

                    1. **Fact-Checking**:
                       - Search the web for credible sources to verify the information in the message.
                       - Identify any factual inaccuracies, misleading statements, or logical inconsistencies.

                    2. **Credibility Score**:
                       - Assign a credibility score to the message on a scale of 0 to 10, where:
                         - 0 = Completely fake or unsupported by evidence.
                         - 5 = Partially true but contains misleading or unverified information.
                         - 10 = Completely true and supported by credible sources.

                    3. **Explanation**:
                       - Provide a detailed explanation of your analysis, including:
                         - Key points from credible sources that support or refute the message.
                         - Any red flags or signs of misinformation.
                         - A summary of why the message is considered real or fake.

                    4. **Recommendations**:
                       - Suggest additional steps the user can take to verify the information (e.g., checking specific websites or sources).

                    ---

                    **Format the response as follows**:
                    - Use clear headings and bullet points for readability.
                    - Include emojis to make the response visually appealing.
                    - Keep the language simple and user-friendly.

                    Message: "{message}"
                """
            }
        ],
    }

        def format_ai_response(response):
            """
            Formats the AI's response into a user-friendly and attractive HTML structure.
            """
            # Split the response into sections
            sections = {
                "Fact-Checking": "",
                "Credibility Score": "",
                "Explanation": "",
                "Recommendations": ""
            }

            # Extract each section from the response
            for section in sections:
                start_tag = f"**{section}:**"
                end_tag = f"**{list(sections.keys())[list(sections.keys()).index(section) + 1]}:**" if list(sections.keys()).index(section) + 1 < len(sections) else ""
                
                # Find the start and end of the section
                start_index = response.find(start_tag)
                end_index = response.find(end_tag) if end_tag else len(response)
                
                if start_index != -1:
                    section_content = response[start_index + len(start_tag):end_index].strip()
                    sections[section] = section_content

            # Format the response with HTML tags
            formatted_response = (
                f"<div class='ai-response'><br>"
                f"<h3>🔍 Fact-Checking Analysis</h3><br>"
                f"<p>{sections['Fact-Checking']}</p><br>"
                f"<h3>📊 Credibility Score</h3><br>"
                f"<p>{sections['Credibility Score']}</p><br>"
                f"<h3>📝 Explanation</h3><br>"
                f"<ul>{''.join([f'<li>{point.strip()}</li>' for point in sections['Explanation'].split('. ') if point.strip()])}</ul><br>"
                f"<h3>✅ Recommendations</h3><br>"
                f"<ul>{''.join([f'<li>{point.strip()}</li>' for point in sections['Recommendations'].split('. ') if point.strip()])}</ul><br>"
                f"</div>"
            )

            return formatted_response
            
        async with aiohttp.ClientSession() as session:
            try:
                async with session.post(OPENROUTER_API_URL, headers=headers, json=payload) as response:
                    if response.status == 200:
                        data = await response.json()
                        ai_response = data["choices"][0]["message"]["content"]
                        formatted_response = format_ai_response(ai_response)
                        return formatted_response
                    return f"Error: {response.status} - {await response.text()}"
            except Exception as e:
                return f"Error analyzing message: {str(e)}"