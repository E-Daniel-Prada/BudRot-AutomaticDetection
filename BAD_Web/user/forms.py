"""
forms file of the alert system project.

Created by BrayanRojas0630, Elkin77, on June 2019.
Copyright (c) 2019 BrayanRojas0630, Elkin77 Corporación Universitaria Minuto de Dios. All rights reserved.

This file is part of ProjectName (BudRot-AutomaticDetection).

ProjectName (BudRot-AutomaticDetection) is free software: you can redistribute it and/or modify it under the terms of the
GNU General Public License as published by the Free Software Foundation, version 3.
"""

from django import forms

class loginForm(forms.Form):
    user_name=forms.CharField(max_length=40, widget=forms.TextInput(attrs=
    	{'type':'text',
    	'class':'form-control form-control-user', 
    	'id':'user_email', 
    	'placeholder':'Enter Email Address...', 
    	'aria-describedby':'emailHelp'
    	}))
    password=forms.CharField(max_length=40, widget=forms.PasswordInput(attrs=
    	{'class':'form-control form-control-user', 
    	'id':'password', 
    	'placeholder':'Password'
    	}))
