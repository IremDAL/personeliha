"""
URL configuration for iha project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.urls import path
from django.urls import re_path as url
from personel import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'), 
    path('personeltransactions/', views.personeltransactions, name='personeltransactions'),
    path('login/', views.login_page, name='login_page'), 
    path('user_login/', views.user_login, name='user_login'),
    path('add_part/', views.add_part, name='add_part'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('parts_list/', views.parts_list, name='parts_list'),  
    path('get_parts/', views.get_parts, name='get_parts'),
    path('aircraft_produce/', views.aircraft_produce, name='aircraft_produce'),
    path('update_part/<int:part_id>/', views.update_part, name='update_part'),  
    path('fetch_aircraft_parts/', views.fetch_aircraft_parts, name='fetch_aircraft_parts'),
    path('update_part_count/', views.update_part_count, name='update_part_count'),
    path('aircraft_produced/', views.aircraft_produced, name='aircraft_produced'),
]
