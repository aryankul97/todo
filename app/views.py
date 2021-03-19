from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from rest_framework.request import Request
from rest_framework.decorators import api_view
from django.http import HttpResponse
from django.core import serializers
from django.db import IntegrityError
from app.models import *
from django.contrib.auth import authenticate

@api_view(['POST', 'PUT'])
@csrf_exempt
def user(request):
	if request.method == 'PUT':
		try:
			data=request.data
			username=data['username']
			email=data['email']
			password=data['password']
			User.objects.create_user(username, email, password)
			return Response({'msg':'User Created Successfully'}, status=status.HTTP_200_OK)
		except IntegrityError:
			return Response({'msg':'User Already Exists'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
	elif request.method == 'POST':
		data=request.data
		username=data['username']
		password=data['password']
		user = authenticate(username=username, password=password)
		if user is not None:
			return Response({'msg':'User Logged In Successfully'}, status=status.HTTP_200_OK)
		else:
			return Response({'msg':'Incorrect Credentials'}, status=status.HTTP_200_OK)

@api_view(['GET', 'POST', 'UPDATE', 'DELETE'])
@csrf_exempt
def todo_task(request):
	data=request.data
	if request.method == 'POST':
		username=data['username']
		task=data['task']
		Tasks(username=username, task=task).save()
		return Response({'msg':'Task Created Successfully'}, status=status.HTTP_200_OK)
	elif request.method == 'GET':
		tasks = serializers.serialize('json', Tasks.objects.filter(username=data['username']))
		return Response(tasks, status=status.HTTP_200_OK)
	elif request.method == 'UPDATE':
		task=data['task']
		completed=data['completed']
		task_id=data['task_id']
		Tasks.objects.filter(id=task_id).update(task=task, completed=completed)
		return Response({'msg':'Updated Successfully'}, status=status.HTTP_200_OK)
	elif request.method == 'DELETE':
		task_id=data['task_id']
		Tasks.objects.filter(id=task_id).delete()
		return Response({'msg':'Deleted Successfully'}, status=status.HTTP_200_OK)