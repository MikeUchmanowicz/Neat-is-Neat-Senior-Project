from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from .services import UserManager

#USER CLASS EXTENDS ABSTRACTBASEUSER
class User(AbstractBaseUser):
    
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    email = models.EmailField(max_length=20, unique=True)
    username = models.CharField(max_length=20, unique=True)
    password = models.CharField(max_length=100)
    is_staff = models.BooleanField(default=False) # admin user;
    is_superuser = models.BooleanField(default=False) # a superuser

    USERNAME_FIELD = 'username'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = [first_name, last_name, email, username, password] 

    objects = UserManager()

    #RETURN NAME
    def get_full_name(self):
        return self.first_name + " " + self.last_name

    #RETURN USERNAME
    def get_username(self):
        return self.username

    #TOSTRING
    def __str__(self):
        return self.username

