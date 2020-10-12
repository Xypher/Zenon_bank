from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, include
from .views import signup, activate, logout, profile
from django.conf.urls import url
from django.contrib.auth.views import LoginView


urlpatterns = [

    path("signup/", signup, name="signup"),
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", logout , name="logout"),
    path("profile/", profile , name="profile"),
    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        activate, name='activate'),

]