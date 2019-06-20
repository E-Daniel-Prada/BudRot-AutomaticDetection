"""

MachineLearning for Early-Alert System project.

Created by Brayan Rojas, Elkin Prada, on June 2019.
Co-workers: Carlos Sierra, Santiago Salazar
Copyright (c) 2019 Brayan Rojas, Elkin Prada Corporación Universitaria Minuto de Dios. All rights reserved.

This file is part of ProjectName (BudRot-AutomaticDetection).

ProjectName (BudRot-AutomaticDetection) is free software: you can redistribute it and/or modify it under the terms of the
GNU General Public License as published by the Free Software Foundation, version 3.

"""
from django.urls import path, include
from django.conf import settings
from . import views
from user import api
from django.views.decorators.csrf import csrf_exempt

app_name = 'usuario'

urlpatterns = [
    path('login/', views.loginUser, name='login'),
    path('user/', views.userPerfil, name='userPerfil'),
    path('', views.index, name='index'),
    path('user_registration/', views.user_registration, name='user_registration'),
    path('get_user_list/', api.GetUserList.as_view(), name="get_user_list"),
    path('add_user/', api.AddUser.as_view(), name="add_user"),
    path('remove_user/', api.RemoveUser.as_view(), name="user_remove"),
    path('edit_user/', api.EditUser.as_view(), name="edit_user"),
    path('active_user/', api.ActiveUser.as_view(), name="active_user"),
    path('user_logout/', views.user_logout, name="user_logout"),

]