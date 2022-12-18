from django.urls import path
from . import views

#URLS FOR USERS APP
urlpatterns = [
    path("logInUser/", views.logInUser, name="login" ),
    path("logOutUser/", views.logOutUser, name="logout" ),
    path("registerUser/", views.registerUser, name="register" )
]
