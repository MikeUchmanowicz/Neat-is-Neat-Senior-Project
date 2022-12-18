from django.db.utils import OperationalError
from django.http import HttpResponse
from django.contrib import messages
from django.shortcuts import render

#Exception Handler for Database Operations
def db_operational_handler(func):
    def inner_function(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except OperationalError:
            messages.error(args[0], ('Error establishing a DB connection. Please see your administrator'))
            return render(args[0], "users/exception.html")
        
    return inner_function
