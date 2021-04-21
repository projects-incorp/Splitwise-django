from django import forms
from django.contrib.auth.models import User
from webapp.models import Transaction_Pairs
#from webapp.models import UserProfileInfo

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta():
        model=User
        fields = ('username','email','password')

class TransactionForm(forms.ModelForm):
    amount = forms.IntegerField()
    number_of_people = forms.IntegerField()
    #Enter the users
    #User1={username}

    class Meta():
        model=Transaction_Pairs
        fields=('amount','number_of_people') #,user1
        

#class UserProfileInfoForm(forms.ModelForm):
   # class Meta():
      #  model=UserProfileInfoFormfields=('portfolio_site','profile_pic')
