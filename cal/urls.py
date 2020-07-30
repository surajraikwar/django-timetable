from django.urls import path
from . import views


app_name = 'cal'

urlpatterns = [
    path("register", views.registration_view, name='register'),
    path('login', views.login_view, name='login')
]
