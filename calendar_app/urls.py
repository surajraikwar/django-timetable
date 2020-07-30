from django.contrib import admin
from django.urls import path, include
from cal import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('', include('cal.urls')),
    path('logout/', views.logout_view, name='logout'),
]
