from django.shortcuts import render, redirect
from django.views import View
import json
from django.http import JsonResponse
from django.contrib.auth.models import User
from validate_email import validate_email
from django.contrib import messages, auth
from userpreferences.models import UserPreference  # Import your UserPreference model

class UsernameValidationView(View):
    def post(self, request):
        data = json.loads(request.body)
        username = data['username']

        if not str(username).isalnum():
            return JsonResponse({'username_error': 'Username should only contain alphanumeric characters'}, status=400)

        if User.objects.filter(username=username).exists():
            return JsonResponse({'username_error': 'Username already taken'}, status=409)

        return JsonResponse({'username_valid': True})


class EmailValidationView(View):
    def post(self, request):
        data = json.loads(request.body)
        email = data['email']

        if not validate_email(email):
            return JsonResponse({'email_error': 'Email is invalid'}, status=400)

        if User.objects.filter(email=email).exists():
            return JsonResponse({'email_error': 'Sorry, email in use, choose another one'}, status=409)

        return JsonResponse({'email_valid': True})


class RegistrationView(View):
    def get(self, request):
        return render(request, 'authentication/register.html')

    def post(self, request):
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']

        context = {
            'fieldValues': request.POST
        }

        if not User.objects.filter(username=username).exists():
            if not User.objects.filter(email=email).exists():
                if len(password) < 6:
                    messages.error(request, 'Password too short')
                    return render(request, 'authentication/register.html', context)

                user = User.objects.create_user(username=username, email=email)
                user.set_password(password)
                user.save()
                messages.success(request, 'Account created successfully')
                return redirect('login')  # Redirect to login page after successful registration

            else:
                messages.error(request, 'Email already in use')
                return render(request, 'authentication/register.html', context)

        else:
            messages.error(request, 'Username already taken')
            return render(request, 'authentication/register.html', context)


class LoginView(View):
    def get(self, request):
        return render(request, 'authentication/login.html')

    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']

        if username and password:
            user = auth.authenticate(username=username, password=password)

            if user:
                auth.login(request, user)
                
                # Check if the user has preferences set
                try:
                    user_preferences = user.userpreference  # Replace with your actual related name
                    if user_preferences.currency:
                        return redirect('expenses')  # Redirect to expenses if preferences are set
                    else:
                        return redirect('preferences')  # Redirect to preferences if preferences are not set
                except UserPreference.DoesNotExist:
                    return redirect('preferences')  # Redirect to preferences if preferences object does not exist

            else:
                messages.error(request, 'Invalid credentials, try again')
                return render(request, 'authentication/login.html')

        else:
            messages.error(request, 'Please fill all fields')
            return render(request, 'authentication/login.html')


class LogoutView(View):
    def post(self, request):
        auth.logout(request)
        messages.success(request, 'You have been logged out')
        return redirect('login')
