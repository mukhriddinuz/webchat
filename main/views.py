from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from chat.models import User, Message, Chat
from django.http.response import JsonResponse
from django.db.models import Q

@login_required
def index(request):
    context = {
        'persons':User.objects.exclude(id=request.user.id),
    }
    return render(request, 'index.html', context)


@login_required
def room(request, room_name):
    return render(request, "room.html", {"room_name": room_name})


@login_required
def get_messages(request):
    recipient_id = request.GET.get('recipient')
    try:
        recipient = User.objects.get(id=recipient_id)
    except (User.DoesNotExist, TypeError, ValueError):
        return JsonResponse({'error': 'Recipient not found or invalid'}, status=400)

    chat = Chat.objects.filter(
        Q(sender=request.user, recipient=recipient) |
        Q(sender=recipient, recipient=request.user),
        is_request=True
    ).first()
    if not chat:
        chat = Chat.objects.create(
            sender=request.user,
            recipient=recipient,
            is_request=True
        )
    chat_data = {
        'sender':chat.sender.id,
    }
    messages = Message.objects.filter(chat=chat, is_deleted__isnull=True).order_by('created_at')
    message_list = []
    for msg in messages:
        message_list.append({
            'id': msg.id,
            'sender': msg.sender.username if msg.sender else None,
            'sender_id': msg.sender.id if msg.sender else None,
            'text': msg.text,
            'created_at': msg.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            'file': msg.file.url if msg.file else None
        })
    print(message_list)
    return JsonResponse({'message': message_list, 'chat_data':chat_data})


