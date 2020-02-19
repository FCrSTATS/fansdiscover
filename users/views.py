from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView


from .forms import CustomUserCreationForm

from .models import Player
from django.db.models import Q


class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'signup.html'

# Create your views here.


class GuideView(CreateView):
    success_url = reverse_lazy('home')
    template_name = 'guide.html'


def players(request):
    players = Player.objects.all()
    contexts = {"players":players}

    return render(request, 'players/players_index.html', {"contexts":contexts})

    
def player_profile(request,pid):
    if request.method == "POST":
        pid = request.POST.get("player")
        # backend check
        print(pid)
        ## NEED TO CREATE PLAYER TABLE IN BACKED
        
    player = Player.objects.filter(pid=pid).values("player")[0]['player']
    position = Player.objects.filter(pid=pid).values("position")[0]['position']
    nationality = Player.objects.filter(pid=pid).values("nationality")[0]['nationality']
    age = Player.objects.filter(pid=pid).values("age")[0]['age']
    market_value = Player.objects.filter(pid=pid).values("value")[0]['value']
    avi = Player.objects.filter(pid=pid).values("avi")[0]['avi']
    print("player is {}".format(player))


    contexts = {"players":player,"positions":position,
                "nationalities":nationality,"ages":age,"market_values":market_value,
                "avi":avi}

    return render(request, 'players/player_profile.html', {"contexts":contexts})