from django.shortcuts import render


# Create your views here.
def index(request):
    return render(request, "chat_app/index.html")


# room_name is getting from index page with jquery codes that set roomName and when we search roomname it help us
# to transfer our search to room view and view get our search
def room(request, room_name):
    context = {
        "room_name": room_name
    }
    return render(request, "chat_app/room.html", context)
