# users/urls.py
from django.urls import path
from .views import SignUpView, GuideView
# from django.views.generic.base import TemplateView

urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    # path('', GuideView.as_view(template_name='guide.html'), name='guide')
]
    
