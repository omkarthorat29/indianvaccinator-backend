"""indianvaccinator URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from . import views
from .FirebaseOps import views as firebaseView
from .Main import view as mainView
from .Cowin import view as cowinView
from .Alerts import view as alertView
from .SendEmail import view as emailView
urlpatterns = [
    path('admin/', admin.site.urls),
    # path('sendalert/',  views.send_alert, name='send_alert'),
    path('alerts/',  alertView.sendAlerts, name='alertView'),
    path('sendEmail/',  emailView.sendEmail, name='emailView'),
    path('cowin/',  cowinView.fetchCenterAndUsers, name='cowinView'),
    path('main/',  mainView.main, name='mainView'),
    path('firebase/', firebaseView.getUsersAndUniquePinocdes, name='getUsersAndUniquePinocdes')
]
