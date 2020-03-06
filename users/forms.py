from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser, Report

class CustomUserCreationForm(UserCreationForm):

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'first_name', 'last_name', 'avatar_url')

class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'first_name', 'last_name', 'avatar_url')


VAL_CHOICES= [
    (10,"10 - World Class Talent"),
    (9,"9 - Big 5 Starter"),
    (8,"8 - Big 5 Squad Player"),
    (7,"7 - Bel / Hol / Port"),
    (6,"6 - DK Superliga Key Player"),
    (5,"5 - DK Superliga Starter"),
    (4,"4 - DK Superliga Squad Player"),
    (3,"3 - 2nd Tier Scandinavia"),
    (2,"2 -Unlikely to Play Pro."),
    (1,"1 - Amateur Career")
    ]


class ReportForm(forms.Form):

    opponent = forms.CharField(max_length=200, required=True)
    date = forms.CharField(max_length=200, required=True)
    report = forms.CharField(widget=forms.Textarea)
    performance_score = forms.CharField(label='Choose a score', widget=forms.Select(choices=VAL_CHOICES))
    potential_score = forms.CharField(label='Choose a score', widget=forms.Select(choices=VAL_CHOICES))
    value_score = forms.CharField(label='Choose a score', widget=forms.Select(choices=VAL_CHOICES))
    
    class Meta:
        model = Report
        fields = ("player","opponent",
                  "date","report","performance_score",
                  "potential_score","value_score")

