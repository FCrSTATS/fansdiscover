from django.shortcuts import render, HttpResponse
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from django.contrib import messages
import json
import base64


from .forms import CustomUserCreationForm, ReportForm, CalibrationForm

from .models import Player, Report, Calibration, Admin
from django.db.models import Q, Avg


class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'signup.html'

# Create your views here.


class GuideView(CreateView):
    success_url = reverse_lazy('home')
    template_name = 'guide.html'



def admin_area(request):
    #get Admin settings:
    settings_instance = Admin.objects.all().filter(settings_instance="master")[0]
    toggle_max_reports = settings_instance.max_reports_toggle
    max_reports = settings_instance.max_reports
    show_user_reports_number = settings_instance.show_user_reports_number
    show_global_reports_number = settings_instance.show_global_reports_number




    reports = Report.objects.all()
    

    contexts = {"toggle_max_reports":toggle_max_reports,
                "max_reports":max_reports,
                "show_user_reports_number":show_user_reports_number,
                "show_global_reports_number":show_global_reports_number, "reports":reports}



    return render(request, 'admin-area.html', {"contexts":contexts})

def admin_toggle(request):
    if request.method == "POST":
        toggle_reports = request.POST.get("toggle_reports")
        max_n = request.POST.get("max_n")
        toggle_user_n = request.POST.get("toggle_user_n")
        toggle_global_n = request.POST.get("toggle_global_n")

        if toggle_reports == "true":
            toggle_reports = True
        else:
            toggle_reports = False
        if toggle_user_n == "true":
            toggle_user_n = True
        else:
            toggle_user_n = False
        if toggle_global_n == "true":
            toggle_global_n = True
        else:
            toggle_global_n = False



        print(toggle_reports,max_n,toggle_user_n,toggle_global_n)

        (Admin.objects
         .all()
         .filter(settings_instance="master")
         .update(max_reports = max_n,
                 max_reports_toggle = toggle_reports,
                 show_user_reports_number = toggle_user_n,
                 show_global_reports_number = toggle_global_n))



        a_dict = {"toggle_reports":toggle_reports, "max_n":max_n}

        return HttpResponse(json.dumps(a_dict), content_type="application/json")





def players(request):
    #get Admin settings:
    settings_instance = Admin.objects.all().filter(settings_instance="master")[0]
    

    toggle_max_reports = settings_instance.max_reports_toggle
    if toggle_max_reports == True:
        max_reports = settings_instance.max_reports
    else:
        max_reports = 1000000


    players = Player.objects.all()

    young_dribblers = Player.objects.filter(report_count__lte=max_reports).filter(age__lte=20).order_by('-dribble')[:10]
    young_dribblers = Player.objects.filter(
        pid__in=young_dribblers
    )
    old_finishers = Player.objects.filter(report_count__lte=max_reports).filter(age__gte=30).order_by('-finish')[:10]
    old_finishers = Player.objects.filter(
        pid__in=old_finishers
    )

    creation_kings = Player.objects.filter(report_count__lte=max_reports).filter(age__lte=20).order_by('-create')[:10]
    creation_kings = Player.objects.filter(
        pid__in=creation_kings
    )


    query = request.GET.get("q")
    if query:
        try:
            q_id = Player.objects.filter(player__contains=query)
            q_id = q_id.values()[0]['pid']
            players = players.filter(
                Q(player__icontains=query)|
                Q(position__icontains=query)|
                Q(team__icontains=query)|
                Q(pid=q_id)).distinct()
        except IndexError:
            players = players.filter(
                Q(player__icontains=query)|
                Q(position__icontains=query)|
                Q(team__icontains=query)).distinct()
        
        try:
            q_id = Player.objects.filter(player__contains=query)
            q_id = q_id.values()[0]['pid']
            young_dribblers = young_dribblers.filter(
                Q(player__icontains=query)|
                Q(position__icontains=query)|
                Q(team__icontains=query)|
                Q(pid=q_id)).distinct()
        except IndexError:
            young_dribblers = young_dribblers.filter(
                Q(player__icontains=query)|
                Q(position__icontains=query)|
                Q(team__icontains=query)).distinct()
        
        try:
            q_id = Player.objects.filter(player__contains=query)
            q_id = q_id.values()[0]['pid']
            old_finishers = old_finishers.filter(
                Q(player__icontains=query)|
                Q(position__icontains=query)|
                Q(team__icontains=query)|
                Q(pid=q_id)).distinct()
        except IndexError:
            old_finishers = old_finishers.filter(
                Q(player__icontains=query)|
                Q(position__icontains=query)|
                Q(team__icontains=query)).distinct()

        try:
            q_id = Player.objects.filter(player__contains=query)
            q_id = q_id.values()[0]['pid']
            creation_kings = creation_kings.filter(
                Q(player__icontains=query)|
                Q(position__icontains=query)|
                Q(team__icontains=query)|
                Q(pid=q_id)).distinct()
        except IndexError:
            creation_kings = creation_kings.filter(
                Q(player__icontains=query)|
                Q(position__icontains=query)|
                Q(team__icontains=query)).distinct()

        


    contexts = {"players":players, "young_dribblers":young_dribblers,
                "old_finishers":old_finishers,"creation_kings":creation_kings}

    return render(request, 'players/players_index.html', {"contexts":contexts})

    
def player_profile(request,pid):

    ## GET ADMIN SETTINGS
    settings_instance = Admin.objects.all().filter(settings_instance="master")[0]

    ## Checking if user numbers and global numbers are set to show

    show_user_n = settings_instance.show_user_reports_number
    show_global_n = settings_instance.show_global_reports_number

    # If show_user_n is True, see if reports exist
    if show_user_n == True:
        try:
            reports = Report.objects.all().filter(user=request.user).filter(player=pid)
            count_reports = len(reports)
            user_avg_perf_score = round(reports.aggregate(Avg('performance_score'))["performance_score__avg"],2)
            user_avg_pot_score = round(reports.aggregate(Avg('potential_score'))["potential_score__avg"],2)
            user_avg_val_score = round(reports.aggregate(Avg('value_score'))["value_score__avg"],2)

            if user_avg_perf_score == None:
                user_avg_perf_score = "-"
            if user_avg_pot_score == None:
                user_avg_pot_score = "-"
            if user_avg_val_score == None:
                user_avg_val_score = "-"
            
        except Exception:
            count_reports = 0
            user_avg_perf_score = "-"
            user_avg_pot_score = "-"
            user_avg_val_score = "-"

    else:
        count_reports = "-"
        user_avg_perf_score = "-"
        user_avg_pot_score = "-"
        user_avg_val_score = "-"

    # If show_global
    if show_global_n == True:
        try:
            reports = Report.objects.all().filter(player=pid).filter(~Q(user = request.user))
            global_count = len(reports)
            global_perf_score = round(reports.aggregate(Avg('performance_score'))["performance_score__avg"],2)
            global_pot_score = round(reports.aggregate(Avg('performance_score'))["performance_score__avg"],2)
            global_val_score = round(reports.aggregate(Avg('performance_score'))["performance_score__avg"],2)

            if global_perf_score == None:
                global_perf_score = "-"
            if global_pot_score == None:
                global_pot_score = "-"
            if global_val_score == None:
                global_val_score = "-"
        
        except Exception:
            global_count = "-"
            global_perf_score = "-"
            global_pot_score = "-"
            global_val_score = "-"
    else:
        global_count = "-"
        global_perf_score = "-"
        global_pot_score = "-"
        global_val_score = "-"

    
        

   
    
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
                                "avi":avi, "form":form,"report_exists":report_exists,
                                "count_reports":count_reports,
                                "user_avg_perf_score":user_avg_perf_score,"user_avg_pot_score":user_avg_pot_score,
                                "user_avg_val_score":user_avg_val_score,"global_perf_score":global_perf_score,
                                "global_pot_score":global_pot_score,"global_val_score":global_val_score,"global_count":global_count}
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

            # Need to increase the report_count in Player model
            report_counts = Report.objects.filter(player=pid).count()
            print(report_counts)
            person = Player.objects.filter(player=player_name).update(report_count=report_counts)


            # Create success boolean and add to contexts to inform user
            success = True
            form = ReportForm
            contexts = {"players":player,"positions":position, "teams":team,
                    "nationalities":nationality,"ages":age,"market_values":market_value,
                    "avi":avi, "success":success,"form":form,"count_reports":count_reports,
                    "user_avg_perf_score":user_avg_perf_score,"user_avg_pot_score":user_avg_pot_score,
                    "user_avg_val_score":user_avg_val_score,"global_perf_score":global_perf_score,
                    "global_pot_score":global_pot_score,"global_val_score":global_val_score,"global_count":global_count}

            return render(request, 'players/player_profile.html', {"contexts":contexts})

    # If this is a GET (or any other method) create the default form.
    else:
        form = ReportForm    
        contexts = {"players":player,"positions":position,"teams":team,
                        "nationalities":nationality,"ages":age,"market_values":market_value,
                        "avi":avi, "form":form,"count_reports":count_reports,"user_avg_perf_score":user_avg_perf_score,
                        "user_avg_pot_score":user_avg_pot_score,"user_avg_val_score":user_avg_val_score,
                        "global_perf_score":global_perf_score,"global_pot_score":global_pot_score,
                        "global_val_score":global_val_score,"global_count":global_count}

        return render(request, 'players/player_profile.html', {"contexts":contexts})
   # form = ReportForm   
    contexts = {"players":player,"positions":position, "teams":team,    
                    "nationalities":nationality,"ages":age,"market_values":market_value,
                    "avi":avi, "form":form,"count_reports":count_reports,"user_avg_perf_score":user_avg_perf_score,
                    "user_avg_pot_score":user_avg_pot_score,"user_avg_val_score":user_avg_val_score,
                    "global_perf_score":global_perf_score,"global_pot_score":global_pot_score,
                    "global_val_score":global_val_score,"global_count":global_count}

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


def reports(request):
    user = request.user
    reports = Report.objects.all().filter(user=user)

    print(reports)
    contexts = {"reports":reports}

    return render(request,"reports.html", {"contexts":contexts})

def read_reports(request,rid):
    reports = Report.objects.all().filter(rid=rid)[0]
    print(reports)
    #rid = reports.values("rid")[0]['rid']
    contexts = {"reports":reports}

    return render(request,"read_report.html", {"contexts":contexts})
    

def delete_report(request,rid):
    """ HANDLING FOR DELETING REPORT WILL GO HERE """
    if request.user.is_superuser:
        report = Report.objects.all().filter(rid=rid)[0]
        player = report.player
        report.delete()
        report_counts = Report.objects.filter(player=player).count()
        Player.objects.filter(player=player).update(report_count=report_counts)


        return HttpResponseRedirect('/admin-area/')

    else:
        pass


