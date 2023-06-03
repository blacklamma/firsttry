from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
import json

# Create your views here.

# rooms = [
#     {'id': 1, 'name': 'Lets learn python!'},
#     {'id': 2, 'name': 'Design with me'},
#     {'id': 3, 'name': 'Frontend developers'},
# ]


def loginPage(request):
    request_data = json.loads(request.body)
    username = request_data.get('username')
    password = request_data.get('password')

    user = authenticate(request, username=username, password=password)

    if user is not None:
        login(request, user)
        return HttpResponse('Login Successful')
    else:
        return HttpResponse('Username OR password is incorrect')


def logoutPage(request):
    request_data = json.loads(request.body)
    username = request_data.get('username')

    user = User.objects.get(username=username)

    if user is not None:
        logout(request)
        return HttpResponse('Logout Successful')
    else:
        return HttpResponse('Error')
