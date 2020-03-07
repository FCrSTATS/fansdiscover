from django.shortcuts import render,HttpResponse
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from django.contrib import messages
import json
import base64


from .forms import CustomUserCreationForm, ReportForm

from .models import Player, Report
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
   
    
    ## THIS IS REALLY INEFFICIENT AND SHOULD BE DONE THROUGH QUERY FILTER
    ## BUT I COULDN'T BE ARSED AND IT'S ONLY FOR ONE PLAYER AT A TIME    
    player = Player.objects.filter(pid=pid).values("player")[0]['player']
    position = Player.objects.filter(pid=pid).values("position")[0]['position']
    nationality = Player.objects.filter(pid=pid).values("nationality")[0]['nationality']
    age = Player.objects.filter(pid=pid).values("age")[0]['age']
    market_value = Player.objects.filter(pid=pid).values("value")[0]['value']
    avi = Player.objects.filter(pid=pid).values("avi")[0]['avi']
    print("player is {}".format(player))

    
    # Getting list of report identifiers to prevent users creating 
    # duplicates for same player in same match
    rids = Report.objects.all().values('rid')
    existing_reports = []
    for r in rids:
        existing_reports.append(r['rid'])


    ### FORM HANDLING:
    
    if request.method == 'POST':
        form = ReportForm(request.POST)
        if form.is_valid():
            report = Report()
            person = Player()
            
            # getting data to create rid
            username = request.user.username
            player_name = player
            p_name = person.__class__.objects.only('pid').get(player=player_name)
            date = form.cleaned_data['date']
            date_string = str(date)
            report_string = player_name+"_"+username+"_"+date_string
            # converting report_string to base64
            report_string = report_string.encode('ascii')
            base64_bytes = base64.b64encode(report_string)
            base64_message = base64_bytes.decode('ascii')

            # if user report for this player in this match exists
            # reload page and add report_exists to contexts
            # so we can warn users.
            if base64_message in existing_reports:
                report_exists = True
                form = ReportForm    
                contexts = {"players":player,"positions":position,
                                "nationalities":nationality,"ages":age,"market_values":market_value,
                                "avi":avi, "form":form,"report_exists":report_exists}
                return render(request, 'players/player_profile.html', {"contexts":contexts})
            
            # if rid does not exist, continue adding to Report model.
            report.user = request.user
            report.rid = base64_message
            report.player = p_name
            report.opponent = form.cleaned_data['opponent']
            report.date = form.cleaned_data['date']
            report.report = form.cleaned_data['report']
            report.performance_score = form.cleaned_data['performance_score']
            report.potential_score = form.cleaned_data['potential_score']
            report.value_score = form.cleaned_data['value_score']
            report.save()

            # Create success boolean and add to contexts to inform user
            success = True
            contexts = {"players":player,"positions":position,
                    "nationalities":nationality,"ages":age,"market_values":market_value,
                    "avi":avi, "success":success}
            return render(request, 'players/player_profile.html', {"contexts":contexts})

    # If this is a GET (or any other method) create the default form.
    else:
        form = ReportForm    
        contexts = {"players":player,"positions":position,
                        "nationalities":nationality,"ages":age,"market_values":market_value,
                        "avi":avi, "form":form}

        return render(request, 'players/player_profile.html', {"contexts":contexts})
   # form = ReportForm   
    contexts = {"players":player,"positions":position,
                    "nationalities":nationality,"ages":age,"market_values":market_value,
                    "avi":avi, "form":form}
    return render(request, 'players/player_profile.html', {"contexts":contexts})

def post_report(request,username):
    rep = {}

    if request.method == "POST":
        username = request.POST.get("username")
        player = request.POST.get("player")
        opponent = request.POST.get("opponent")
        date = request.POST.get("date")
        user_report = request.POST.get("report")
        performance = request.POST.get("performance")
        potential = request.POST.get("potential")
        value_score = request.POST.get("value_score")

        report = Report()
        report.player = player
        report.opponent = opponent
        report.date = date
        report.report = user_report
        report.performance_score = performance
        report.potential_score = potential
        report.value_score = value_score
        report.save()
        print("report data saved")
        rep = {"username":username,"player":player}
        return HttpResponse(json.dumps(rep), content_type="application/json")
    
    return HttpResponse(json.dumps(rep), content_type="application/json")