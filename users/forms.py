from django.contrib.auth.forms import UserCreationForm
from .models import EmailUser

class EmailUserCreation(UserCreationForm):
    class Meta:
        model= EmailUser
        fields=('email' , 'password1' , 'password2')