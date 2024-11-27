from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import check_password

# Create your views here.

def signin(request):
    if request.method == 'POST':
        user_username = request.POST.get('username')
        user_psw = request.POST.get('psw')

        try:    
            user = get_object_or_404(User, username = user_username)
            user = User.objects.filter(username = user_username).first()

            print(user)
            login_user = authenticate(username = user_username, password = user_psw)
            login(request, login_user)
            return redirect('/dashboard/')
        except:
            return HttpResponse('Credentials Match Failed! - Try Logging In using correct credentials -- ')
        
    return render(request, 'login.html')

def register(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        username = request.POST.get('username')
        psw = request.POST.get('psw')
        cpsw = request.POST.get('cpsw')

        if psw != cpsw or len(psw) < 8:
            return HttpResponse('Password Error! - Please make sure password match the conditions!')

        try:
            user = User.objects.create(
                username = username,
                email = email,
            )

            user.set_password(psw)
            user.save()

            return redirect('/sign-in/')
        except:
            return HttpResponse('Facing Server Issues! -- Please retry --')

    return render(request, 'register.html')

@login_required(login_url='/sign-in/')
def changePassword(request):
    if request.method == 'POST':

        raw_password = request.POST.get('old-psw')
        new_password = request.POST.get('new-psw')
        cnew_password = request.POST.get('new-cpsw')

        if new_password != cnew_password or len(new_password) < 8:
            return HttpResponse('Passwords don\'t match the conditions! - Try Again!')

        user = User.objects.get(username = request.user)
        
        try:
            if check_password(raw_password, user.password):
                print('Changed password')
                user.set_password(new_password)
                user.save()
                logout(request)
                return HttpResponse('Password Changed Successfully! - Try Signing In Again!')
        except:
            return redirect('/change-password/')

    return render(request, 'changePassword.html')

@login_required(login_url='/sign-in/')
def signOut(request):
    logout(request)
    return redirect('/')