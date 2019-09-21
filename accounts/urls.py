from django.urls import path
from django.conf.urls import url
from . import views
from .forms import LoginForm

app_name = 'account'

urlpatterns = [
    path(r'register/', views.RegisterView.as_view(success_url='/'), name='register'),
    path(r'account/result.html', views.account_result, name='result'),
    path(r'login/', views.LoginView.as_view(success_url='/'), name='login', kwargs={'authentication': LoginForm})


]
