from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login as auth_login, logout, authenticate
from . forms import *
from . exceptions import db_operational_handler

#LOGIN VIEW
@db_operational_handler # EXCEPTION HANDLER WRAPPING FUNCTION
def logInUser(request):
    form = UserLoginForm()
    
    #IF USER SUBMITS FORM
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)

        #IF FORM VALID
        if form.is_valid():
        
            #CHECK IF USER EXISTS USING GIVEN CREDENTIALS
            username=form.cleaned_data['username']
            password=form.cleaned_data['password']
            user=authenticate(username=username, password=password)
        
            #IF USER EXISTS
            if user is not None:
                #LOG USER IN
                auth_login(request, user)
                messages.success(request, (f'Logged In. Welcome {username.upper()}!'))
                return redirect("home")
            else:
                messages.error(request, ("Username / Password Combination Invalid"))
    
    #BASE CASE
    #IF USER ENTERS PAGE / DOES NOT SUBMIT FORM / FORM INVALID / USER DOES NOT EXIST
    context = {'form':form}
    return render(request, "users/login.html", context)


#LOGOUT VIEW
@db_operational_handler # EXCEPTION HANDLER WRAPPING FUNCTION
def logOutUser(request):
    
    #LOGOUT USER
    logout(request)
    messages.warning(request, ("User Logged Out"))
    return render(request, "main/home.html")


#REGISTER VIEW
@db_operational_handler # EXCEPTION HANDLER WRAPPING FUNCTION
def registerUser(request):
    form = UserRegistrationForm()
    
    #IF USER SUBMIT FORM
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        
        #IF FORM IS VALID
        if form.is_valid():
            
            User = form.save()
            username = form.cleaned_data['username']
            messages.success(request, (f'Account Created. Welcome {username.upper()}!'))
            return redirect("home")
    
    #BASE CASE
    #IF USER ENTERS PAGE / DOES NOT SUBMIT FORM / FORM INVALID
    context = {'form':form}
    return render(request, "users/register.html", context)
        