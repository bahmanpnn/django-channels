import json

from django.shortcuts import render
from django.utils.safestring import mark_safe


# Create your views here.
def index(request):
    return render(request, "chat_app/index.html")


# room_name is getting from index page with jquery codes that set roomName and when we search roomname it help us
# to transfer our search to room view and view get our search
def room(request, room_name):
    username = request.user.username
    context = {
        "room_name": room_name,
        "username": mark_safe(json.dumps(username))
    }
    return render(request, "chat_app/oldroom.html", context)
