from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login as auth_login, logout, authenticate
from . forms import *
from . exceptions import db_operational_handler

#LOGIN VIEW
@db_operational_handler
def logInUser(request):
    form = UserLoginForm()
    
    #IF USER SUBMITS FORM
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)

        #IF FORM VALID
        if form.is_valid():
        
            #AUTHENTICATE USER WITH FORM CREDENTIALS
            username=form.cleaned_data['username']
            password=form.cleaned_data['password']
            user=authenticate(username=username, password=password)
        
            #IF USER (FORM) DOES NOT EXIST
            if user is None:
                messages.error(request, ("Username / Password Combination invalid"))
                context = {'form':form}
                return render(request, "users/login.html", context)
        
            #LOG USER IN
            auth_login(request, user)
            messages.success(request, (f' Welcome {username.upper()}!'))
            return redirect("/")

        #FORM NOT VALID    
        context = {'form':form}
        return render(request, "users/login.html", context)
    
    #IF REQUEST = "GET"
    context = {'form':form}
    return render(request, "users/login.html", context)

#LOGOUT VIEW
def logOutUser(request):
    
    #LOGOUT USER
    logout(request)
    messages.warning(request, ("User Logged Out"))
    return render(request, "main/home.html")

#REGISTER VIEW
def registerUser(request):
    form = UserRegistrationForm()
    
    #IF USER SUBMIT FORM
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        
        #IF FORM IS VALID
        if form.is_valid():
            User = form.save()
            context = {'user':form.cleaned_data['username']}
            messages.success(request, 'Profile Created.')
            return render(request, "users/registerSuccess.html", context)
        
        #FORM NOT VALID
        context = {'form':form}
        return render(request, "users/register.html", context)
        
    #IF USER DOES NOT SUBMIT FORM
    context = {'form':form}
    return render(request, "users/register.html", context)
        