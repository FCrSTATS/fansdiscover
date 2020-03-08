from django.shortcuts import render, HttpResponse
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from django.contrib import messages
import json
import base64


from .forms import CustomUserCreationForm, ReportForm, CalibrationForm

from .models import Player, Report, Calibration
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
    team = Player.objects.filter(pid=pid).values("team")[0]['team']
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
                #form = ReportForm    
                contexts = {"players":player,"positions":position,"teams": team,
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
            form = ReportForm
            contexts = {"players":player,"positions":position, "teams":team,
                    "nationalities":nationality,"ages":age,"market_values":market_value,
                    "avi":avi, "success":success,"form":form}
            return render(request, 'players/player_profile.html', {"contexts":contexts})

    # If this is a GET (or any other method) create the default form.
    else:
        form = ReportForm    
        contexts = {"players":player,"positions":position,"teams":team,
                        "nationalities":nationality,"ages":age,"market_values":market_value,
                        "avi":avi, "form":form}

        return render(request, 'players/player_profile.html', {"contexts":contexts})
   # form = ReportForm   
    contexts = {"players":player,"positions":position, "teams":team,    
                    "nationalities":nationality,"ages":age,"market_values":market_value,
                    "avi":avi, "form":form}
    return render(request, 'players/player_profile.html', {"contexts":contexts})


def send_calibration(request):
    if request.method == "POST":
        user = request.user
        username = user.username
        scores = request.POST.get("scores")
        
        if "Entry" in scores:
            print("Entry is in scores")
            error = True
            contexts = {"error":error}
            return HttpResponseRedirect('/calibrate-opinion', {"contexts":contexts})
        
        calibrate = Calibration()
        calibrate.user = user
        calibrate.calibration_array = scores
        calibrate.save()

        print(scores)

        a_dict = {"user":username, "scores":scores}

        return HttpResponse(json.dumps(a_dict), content_type="application/json")

        


def calibration(request):
        
    if request.method == 'POST':
        form = CalibrationForm(request.POST)
        if form.is_valid():
            calibration = Calibration()
            # getting data to create rid
            username = request.user.username
            
            # if rid does not exist, continue adding to Report model.
            calibration.user = request.user
            calibration.performance_score = form.cleaned_data['performance_score']
            calibration.potential_score = form.cleaned_data['potential_score']
            calibration.value_score = form.cleaned_data['value_score']
            calibration.save()

            """# Create success boolean and add to contexts to inform user
            success = True
            form = ReportForm
            contexts = {"players":player,"positions":position, "teams":team,
                    "nationalities":nationality,"ages":age,"market_values":market_value,
                    "avi":avi, "success":success,"form":form}
            return render(request, 'players/player_profile.html', {"contexts":contexts})
            """
        # If this is a GET (or any other method) create the default form.
        else:
            form = CalibrationForm    
            contexts = {"form":form}
            return render(request, 'calibrate.html', {"contexts":contexts})
    form = CalibrationForm   
    contexts = {"form":form}
    return render(request, 'calibrate.html', {"contexts":contexts})


