from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView


from .forms import CustomUserCreationForm

class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'signup.html'

# Create your views here.


class GuideView(CreateView):
    success_url = reverse_lazy('home')
    template_name = 'guide.html'

    
def player_profile(request,player):
    if request.method == "POST":
        player = request.POST.get("player")
        # backend check
        print(player)
        ## NEED TO CREATE PLAYER TABLE IN BACKED
        

    contexts = {"player":player}

    return render(request, 'players/player_profile.html', {"contexts":contexts})