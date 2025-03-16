from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.conf import settings
import os
import random
from django.urls import reverse_lazy
from chat_app.forms import AddUserToChatForm
from .models import ChatRoom
from django.db.models import Q
from .models import ChatMessage

# Create your views here.
@login_required
def chat_landing(request, user_name):
    user = get_object_or_404(User, username=user_name)
    if request.method == 'POST':
        form = AddUserToChatForm(request.POST, request=request)
        if form.is_valid():
            
            selected_user = form.cleaned_data['user2']

            chat_room, created = ChatRoom.objects.get_or_create(
                user1=request.user,
                user2=selected_user,
                defaults={'name': f"Chat: {request.user.username} & {selected_user.username}"}
            )

            if created:
                messages.success(request, f"Chat created with {selected_user.username}")
            else:
                messages.warning(request, "Chat room already exists!")

            return redirect('Chat-Landing', user_name=user_name)

    else:
        form = AddUserToChatForm(request=request)

    # Fetch chats where the user is either user1 or user2
    chat_rooms = ChatRoom.objects.filter(Q(user1=request.user) | Q(user2=request.user))

    context = {
        'form': form,
        'chat_rooms': chat_rooms
    }
    return render(request, "chat/chat_landing.html", context)
    


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
    reverse=True
)

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