from django.contrib.auth.base_user import BaseUserManager
#For Managing the Creation and Authentication of Users
class UserManager(BaseUserManager):
    
    def createUser(self, first_name, last_name, email, username, password, **extra_fields):
        #CREATE AND SAVE A USER TO DATABASE.
        user = self.model(username=username, first_name=first_name, last_name=last_name, email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user
    
        