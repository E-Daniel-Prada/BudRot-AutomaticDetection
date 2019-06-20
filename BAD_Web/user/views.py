"""

MachineLearning for Early-Alert System project.

Created by Brayan Rojas, Elkin Prada, on June 2019.
Co-workers: Carlos Sierra, Santiago Salazar
Copyright (c) 2019 Brayan Rojas, Elkin Prada Corporación Universitaria Minuto de Dios. All rights reserved.

This file is part of ProjectName (BudRot-AutomaticDetection).

ProjectName (BudRot-AutomaticDetection) is free software: you can redistribute it and/or modify it under the terms of the
GNU General Public License as published by the Free Software Foundation, version 3.

"""

from django.contrib.auth import authenticate
from django.contrib.auth import login
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render
from .forms import loginForm
from rest_framework.authtoken.models import Token
from network.models import Alert, Upload, Image
from django.contrib.auth.models import User


# Create your views here.
def loginUser(request):
    login_form=loginForm()
    if request.method=='POST':

        form = loginForm(request.POST)
        if form.is_valid():
            username=request.POST['user_name']
            password=request.POST['password']
            print ("user=", username, "password=", password)
            user = authenticate(request=request, username=username, password=password)
            Token.objects.get_or_create(user=user)
            if user is not None and user.is_active:
                request.session.set_expiry(86400)
                login(request, user)
                return HttpResponseRedirect('/user')
            else:
                fail="Usuario o contraseña invalidos!"
                return render(request,'login.html',{"form":login_form, "fail":fail})
    return render(request,'login.html',{"form":login_form})


@login_required(login_url='/')
def userPerfil(request):
    context = {}
    context['alerts'] = Alert.objects.count()
    context['upload'] = Upload.objects.count()
    context['images_processed'] =  Image.objects.filter(status_file = 3).count()
    context['images_not_processed'] =  Image.objects.filter(status_file = 0).count()
    context['users'] = User.objects.count()
 
    return render(request,'user.html', context)


def index(request):
    return render(request, 'index.html')

@login_required(login_url='/')
def user_registration(request):

    return render(request, 'user/user_registration.html')



@login_required
def user_logout(request):
    # Since we know the user is logged in, we can now just log them out.
    logout(request)
    return render(request, 'index.html')
    # Take the user back to the homepage.