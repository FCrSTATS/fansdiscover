"""fd URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.views.generic.base import TemplateView

from django.conf.urls import url
from users import views

urlpatterns = [
    path('', TemplateView.as_view(template_name='home.html'), name='home'),
    path('home', TemplateView.as_view(template_name='home.html'), name='home2'),
    path('guide', TemplateView.as_view(template_name='guide.html'), name='guide'),
    # path('critical-questions', TemplateView.as_view(template_name='questions.html'), name='questions'),
    path('scoring-system', TemplateView.as_view(template_name='scoring.html'), name='scoring'),
  #  path('reports', TemplateView.as_view(template_name='reports.html'), name='reports'),
    path('critical-questions', TemplateView.as_view(template_name='questions.html'), name='questions'),
    path('calibrate-opinion', views.calibration, name='calibrate'),
  #  path('players/', TemplateView.as_view(template_name='players/players_index.html'), name='players_home'),
    path('kudus', TemplateView.as_view(template_name='players/kudus.html'), name='kudus'),
    # path('guide/', TemplateView.as_view(template_name='guide.html'), name='guide'),
    path('admin/', admin.site.urls),
    path('users/', include('users.urls')),
    path('users/', include('django.contrib.auth.urls')),
    url('players',views.players, name="player_list"),
    url(r'^player_profile/(?P<pid>\w+)/$',views.player_profile, name="player_profile"),
    url(r'^send_calibration/$', views.send_calibration, name="send_calibration"),
    url(r'^admin-area/$', views.admin_area, name="admin-area"),
    url(r'^send_admin_toggle/$', views.admin_toggle, name="admin-toggle"),
    url(r'^reports/(?P<rid>\w+)/$', views.read_reports, name="reports"),
    url(r'^reports/$', views.reports, name="reports"),
    url(r'^delete_report/(?P<rid>\w+)/$', views.delete_report, name="delete_report"),
]
