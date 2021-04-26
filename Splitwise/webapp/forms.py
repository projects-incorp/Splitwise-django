from django import forms
from django.contrib.auth.models import User
from webapp.models import Transaction_Pairs
from webapp.models import Transaction_history
#from webapp.models import UserProfileInfo

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta():
        model=User
        fields = ('username','email','password')

class TransactionForm(forms.ModelForm):

    people=forms.CharField()
    #Enter the users
    #User1={username}

    class Meta():
        model=Transaction_Pairs
        fields=('amount',)


class HistForm(forms.ModelForm):
    class Meta():
        model=Transaction_history
        fields=('date','reason')

#class UserProfileInfoForm(forms.ModelForm):
   # class Meta():
      #  model=UserProfileInfoFormfields=('portfolio_site','profile_pic')
