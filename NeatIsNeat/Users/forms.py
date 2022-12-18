from django import forms  
from .models import User
from django.contrib.auth.forms import UserCreationForm  , AuthenticationForm, UsernameField
from django.core.exceptions import ValidationError  

#USER REGISTRATION FORM EXTENDS DJANGO.forms
class UserRegistrationForm(forms.Form):
    #CONFIG CLASS
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'username', 'password1', 'password2')
        
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder':'First Name', 'style':'width:25%'}),
        required='true', min_length='3', max_length='20')
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Last Name', 'style':'width:25%'}),
        required='true', min_length='3', max_length='20')
    email = forms.EmailField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Email', 'style':'width:25%'}),
        required='true', min_length='3', max_length='20')
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Username', 'style':'width:25%'}),
        required='true', min_length='3', max_length='20')
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder':'Password', 'style':'width:25%'}), 
        label = 'Password', required='true', min_length='8', max_length='20')
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder':'Confirm Password', 'style':'width:25%'}), 
        label = 'Confirm Password', required='true', min_length='8', max_length='20', help_text=("Enter the same password again"))

    #SAVE USER USING USER MANAGER
    def save(self, commit = True):
        if commit:  
            user = User.objects.createUser(
                self.cleaned_data['first_name'],
                self.cleaned_data['last_name'],
                self.cleaned_data['email'],   
                self.cleaned_data['username'],  
                self.cleaned_data['password2'],
            )  
            return user
    
    #CLEAN FIRST NAME
    def clean_first_name(self):  
        first_name = self.cleaned_data['first_name'].lower()   
        return first_name  
    
    #CLEAN LAST NAME
    def clean_last_name(self):  
        last_name = self.cleaned_data['last_name'].lower()  
        return last_name 
    
    #CLEAN USERNAME
    def clean_username(self):  
        username = self.cleaned_data['username'].lower()
        new = User.objects.filter(username = username)  
        if new.count():  
            raise ValidationError(" User \"{u}\" already exists".format(u = username))  
        return username     
  
    #CLEAN EMAIL
    def clean_email(self):  
        email = self.cleaned_data['email'].lower()    
        new = User.objects.filter(email=email)  
        if new.count():  
            raise ValidationError(" Email \"{e}\" already exists".format(e = email))   
        return email    
    
    #CLEAN PASSWORD
    def clean_password2(self):  
        password1 = self.cleaned_data['password1']  
        password2 = self.cleaned_data['password2']
        if password1 and password2 and password1 != password2:  
            raise ValidationError({"Passwords don't match"})  
        return password2  
    
    
#USER LOGIN EXTENDS DJANGO.forms
class UserLoginForm(forms.Form):
 
    #CONFIG CLASS
    class Meta:
        model = User
        fields = ('username', 'password')
        
    username = UsernameField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder':'Username', 'style':'width:25%'}), required='true')
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'placeholder':'Password', 'style':'width:25%'}), required='true')

    #CLEAN USERNAME
    def clean_username(self):  
        username = self.cleaned_data['username'].lower()  
        return username
    
    #CLEAN PASSWORD    
    def clean_password(self):  
        password = self.cleaned_data['password']  
        return password
    
