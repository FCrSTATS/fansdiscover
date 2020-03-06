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


class ReportForm(forms.Form):
    player = forms.CharField(max_length=200)
    opponent = forms.CharField(max_length=200, required=True)
    date = forms.DateField()
    report = forms.Textarea()
    performance_score = forms.Select()
    potential_score = forms.Select()
    value_score = forms.Select()

    class Meta:
        model = Report
        fields = ("player","opponent",
                  "date","report","performance_score",
                  "potential_score","value_score")