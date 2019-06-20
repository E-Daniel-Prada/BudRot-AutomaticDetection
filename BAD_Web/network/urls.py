"""
urls file of the neural network phase.

Created by BrayanRojas0630, Elkin77, on June 2019.
Copyright (c) 2019 BrayanRojas0630, Elkin77 Corporación Universitaria Minuto de Dios. All rights reserved.

This file is part of ProjectName (BudRot-AutomaticDetection).

ProjectName (BudRot-AutomaticDetection) is free software: you can redistribute it and/or modify it under the terms of the
GNU General Public License as published by the Free Software Foundation, version 3.
"""

from django.conf import settings
from django.urls import path, include
from . import views
from network.views import Simulation
from network import api
app_name = 'network'

urlpatterns = [
   
   path('simulation/', views.main, name='simulation'),
   path('load_file/', views.load_file, name='load_file'),
   path('upload_images/', api.UploadImages.as_view(), name='load_file'),
   path('get_upload_list/', api.GetUploadList.as_view(), name="get_upload_list"),
   path('get_alert_list/', api.GetAlertList.as_view(), name="get_alert_list"),
   path('list_alerts/', views.list_alerts, name="list_alerts"),
   path('process/', api.RunThread.as_view(), name="process/"),
]