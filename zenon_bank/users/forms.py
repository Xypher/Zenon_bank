from django.contrib.auth.forms import UserCreationForm, User
from django.contrib.auth.models import User
from django.forms import ModelForm, ValidationError
from .models import Student, Profile
from validate_email import validate_email

class UserForm(UserCreationForm):

    class Meta:
        model= User
        fields = ["username", "email", "first_name", "last_name", "password1", "password2"]
    
    """
    def clean_email(self):
        
        
        cd = self.cleaned_data
        return cd
        email = cd["email"]

        if "@" not in email or email[email.find("@"):] != "@ju.edu.jo":
            error_messege = "Email Entered should be something like example@ju.edu.jo"

            raise ValidationError(error_messege) 

        return cd
    """
    

class StudentCreationForm(ModelForm):

    class Meta:
        model = Student
        fields = ["department", "phone_number", "gender", "biography"]





class UserUpdateForm(ModelForm):

    class Meta:
        model=User
        fields=["first_name", "last_name", "username"]


class StudentUpdateForm(ModelForm):

    class Meta:
        model=Student
        fields=["phone_number", "department", "gender", "biography"]
    


class ProfileUpdateForm(ModelForm):
    
    class Meta:
        model = Profile
        fields=["profile_img"]

    



