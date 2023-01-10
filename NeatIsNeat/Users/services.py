from django.contrib.auth.base_user import BaseUserManager
#For Managing the Creation and Authentication of Users
class UserManager(BaseUserManager):
    
    def create_user(self, first_name, last_name, email, username, password, **extra_fields):
        #CREATE AND SAVE A USER TO DATABASE.
        user = self.model(username=username, first_name=first_name, last_name=last_name, email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user
    
    def create_superuser(self, username, password, **extra_fields):

        if password is None:
            raise TypeError('Superusers must have a password.')

        user = self.model(username=username, **extra_fields)
        user.is_superuser = True
        user.is_staff = True
        user.save()

        return user
    
        