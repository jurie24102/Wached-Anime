from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib import messages
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.contrib.auth import get_user_model
import json

from django.core.exceptions import ValidationError

@csrf_exempt
def register_user(request):
    User = get_user_model()
    if request.method == 'POST':
        data = json.loads(request.body)
        username = data['username']
        password = data['password1']
        password2 = data['password2']
        email = data['email']
        errors = {}

        if User.objects.filter(username=username).exists():
            errors['username'] = 'Username is already taken'
        if User.objects.filter(email=email).exists():
            errors['email'] = 'Email is already taken'
        if password != password2:
            errors['password2'] = 'Passwords do not match'

        if errors:
            return JsonResponse({'success': False, 'errors': errors}, status=400)

        try:
            user = User.objects.create_user(username=username, password=password, email=email)
            user.save()
            return JsonResponse({'success': True, 'message': f'You are now registered and can log in as {username}'}, status=201)
        except ValidationError as e:
            return JsonResponse({'success': False, 'errors': e.message_dict}, status=400)

    return JsonResponse({'success': False, 'message': 'Invalid request'}, status=400)

def index(request):
    if request.user.is_authenticated:
        return render(request, 'index.html')
    else:
        return redirect('login')

def login_user(request):
    User = get_user_model()
    if request.method == 'POST':
        data = json.loads(request.body)
        email = data['email']
        password = data['password']
        errors = {}

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            errors['email'] = 'Invalid email or password'
            return JsonResponse({'success': False, 'errors': errors}, status=400)
        else:
            if user.check_password(password):
                login(request, user)
                return JsonResponse({'success': True, 'message': f'You are now logged in as {user.username}'}, status=200)
            else:
                errors['password'] = 'Invalid email or password'
                return JsonResponse({'success': False, 'errors': errors}, status=400)

    return JsonResponse({'success': False, 'message': 'Invalid request'}, status=400)

def logout_user(request):
    logout(request)
    messages.success(request, 'You are now logged out')
    return redirect('login')





def get_all_users(request):
    users = User.objects.all()
    users_list = list(users.values('username', 'email'))  # add more fields if needed
    return JsonResponse(users_list, safe=False)