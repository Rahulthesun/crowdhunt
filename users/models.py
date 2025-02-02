from django.db import models
from django.contrib.auth.models import BaseUserManager , AbstractBaseUser , PermissionsMixin

# Create your models here.

class EmailUserManager(BaseUserManager):
    def create_user(self , email , password=None):
        if not email:
            raise ValueError("Please Provide a Valid Email")
        if not password:
            raise ValueError("Invalid Password")
        email = self.normalize_email(email=email)
        user = self.model(email=email)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self , email , password=None):
        if not email:
            raise ValueError("Please Provide a Valid Email")
        if not password:
            raise ValueError("Invalid Password")
        user = self.create_user(email=email , password=password)
        user.is_staff = True
        user.is_superuser = True
        user.save()
        return user


class EmailUser(AbstractBaseUser , PermissionsMixin):
    id=models.AutoField(primary_key=True)
    email = models.EmailField(unique=True , max_length=60)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    
    date_signed_up = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []


    objects = EmailUserManager()

    def __str__(self):
         return self.email