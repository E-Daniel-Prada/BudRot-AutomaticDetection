"""
user api of the alert system project.

Created by BrayanRojas0630, Elkin77, on June 2019.
Copyright (c) 2019 BrayanRojas0630, Elkin77 Corporación Universitaria Minuto de Dios. All rights reserved.

This file is part of ProjectName (BudRot-AutomaticDetection).

ProjectName (BudRot-AutomaticDetection) is free software: you can redistribute it and/or modify it under the terms of the
GNU General Public License as published by the Free Software Foundation, version 3.
"""

from datetime import datetime
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse, StreamingHttpResponse
from rest_framework.views import APIView
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from network.models import Upload, Image
import os
from os.path import dirname, exists
from sys import argv
from zipfile import BadZipfile, ZipFile
from django.conf import settings
from django.utils.timezone import localtime
import json
import boto3
from django.contrib.auth.models import User

class GetUserList(APIView):
	def get(self, request):
		data = request.data
		print ("<<<<<<<>", "llegue")
		file_list = []
		user_objs = User.objects.all()
		for user in user_objs:
			obj = {}
			obj['id'] = user.id
			obj['username'] = user.username
			obj['is_superuser'] = user.is_superuser
			obj['first_name'] = user.first_name
			obj['last_name'] = user.last_name
			obj['email'] = user.email
			obj['is_activate'] = user.is_active
			obj['last_login'] = localtime(user.last_login).strftime("%Y-%d-%m %I:%M %p")
			file_list.append(obj)
			context = {
			'file_list':file_list
			}
		return HttpResponse(json.dumps(context), content_type="application/json")


class RemoveUser(APIView):
	def post(self, request):
		data = request.data
		user = User.objects.get(id = data['id'])
		user.delete()
		return HttpResponse(json.dumps({'status':'success'}), content_type="application/json")

class ActiveUser(APIView):
	def post(self, request):
		data = request.data
		user = User.objects.get(id = data['id'])
		if user.is_active == True:
			user.is_active = False
		else:
			user.is_active = True
		user.save()
		return HttpResponse(json.dumps({'status':'success'}), content_type="application/json")

class AddUser(APIView):
	def post(self, request):
		data = request.data
		user = User()
		user.first_name = data['first_name']
		user.last_name = data['last_name']
		user.email = data['email']
		user.username = data['username']
		user.password = data['password']
		user.is_superuser = True
		user.save()
		return HttpResponse(json.dumps({'status':'success'}), content_type="application/json")

class EditUser(APIView):
	def post(self, request):
		data = request.data
		user = User.objects.get(id = data.id_user)
		user.first_name = data.name
		user.last_name = data.last_name
		user.email = data.email
		user.username = data.username
		user.password = data.password
		user.is_superuser = True
		user.save()
		return HttpResponse(json.dumps(json.dumps({'status':'success'})), content_type="application/json")