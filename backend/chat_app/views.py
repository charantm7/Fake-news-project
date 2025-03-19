from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.conf import settings
import os
import random
import requests
import json
from django.urls import reverse_lazy
from chat_app.forms import AddUserToChatForm
from .models import ChatRoom
from django.db.models import Q
from .models import ChatMessage
from channels.generic.websocket import AsyncWebsocketConsumer
from datetime import datetime


OPENROUTER_API_KEY = "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" 
OPENROUTER_API_URL = "https://openrouter.ai/api/v1/chat/completions"

# Create your views here.
@login_required
def chat_landing(request, user_name):
    user = User.objects.exclude(id=request.user.id)
    
    return render(request, "chat/chat_landing.html",{'users':user} )

def analyze_message_with_mistral(message: str) -> str:
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
    response = requests.post(OPENROUTER_API_URL, headers=headers, json=payload)
    if response.status_code == 200:
        return response.json()["choices"][0]["message"]["content"]
    return f"Error: {response.status_code} - {response.text}"
    


@login_required
def chat(request, chat_name):
    search_query = request.GET.get('search', '') 
    users = User.objects.exclude(id=request.user.id) 
    chats = ChatMessage.objects.filter(
        (Q(sender=request.user) & Q(receiver__username=chat_name)) |
        (Q(receiver=request.user) & Q(sender__username=chat_name))
    )

    if search_query:
        chats = chats.filter(Q(content__icontains=search_query))  

    chats = chats.order_by('timestamp') 
    user_last_messages = []

    for user in users:
        last_message = ChatMessage.objects.filter(
            (Q(sender=request.user) & Q(receiver=user)) |
            (Q(receiver=request.user) & Q(sender=user))
        ).order_by('-timestamp').first()

        user_last_messages.append({
            'user': user,
            'last_message': last_message
        })

    user_last_messages.sort(
    key=lambda x: (x['last_message'] is not None, x['last_message'].timestamp if x['last_message'] else 0),
    reverse=True)
    


    return render(request, 'chat/chat.html', {
        
        'room_name': chat_name,
        'chats': chats,
        'users': users,
        'user_last_messages': user_last_messages,
        'search_query': search_query 
    })

    

def dashboard(request):
    if request.user.is_authenticated:
        return render(request, 'dashboard/dash.html')
    else:
        messages.error(request, 'You are not logged in')
        return redirect(f'{reverse("Auth")}?action=login')
    

def search_users(request):
    query = request.GET.get("q", "")
    if query:
        users = User.objects.filter(Q(username__icontains=query))[:10]
        results = [{"id": user.id, "text": user.username} for user in users]
    else:
        results = []

    return JsonResponse({"results": results}) 




