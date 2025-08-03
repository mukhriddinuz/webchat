from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from chat.models import User

@login_required
def index(request):
    context = {
        'persons':User.objects.exclude(id=request.user.id),
    }
    return render(request, 'index.html', context)



@login_required
def get_messages(reqeust):
    pass