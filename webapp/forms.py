from django import formsfrom django.contrib.auth.models import User
#from webapp.models import UserProfileInfo
from django import forms
class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta():
        model=Userfields =('username','email','password')

#class UserProfileInfoForm(forms.ModelForm):
   # class Meta():
      #  model=UserProfileInfoFormfields=('portfolio_site','profile_pic')