# -*- coding: utf-8 -*-
"""mysite URL Configuration

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
from django.urls import path , re_path
from . import views
from django.contrib.auth import views as auth_views

app_name = "main"

urlpatterns = [
	path("",views.homepage,name="homepage"),
	path("register/",views.register,name="register"),
	path("logout/",views.logout_request,name="logout"),
	path("login/",views.login_request,name="login"),
    path("chat/",views.index,name="index"),
    path("editPost/",views.editPost,name="editPost"),
    path("backstage/",views.backstage,name="backstage"),
    path("editPostDone/",views.editPostDone,name="editPostDone"),
    path("<single_slug>",views.single_slug,name="single_slug"),
    path('zarinpal/request/', views.send_request, name='request'),
    path('zarinpal/verify/', views.verify , name='verify'),
    path("donate/",views.donate,name="donate"),
    path("removeIdea/",views.removeIdea,name="removeIdea"),
    path("addcomments/",views.addcomments,name="addcomments"),
    path("replaycomments/",views.replaycomments,name="replaycomments"),


]
