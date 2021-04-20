from django import forms
from django.contrib.auth.models import User
#from webapp.models import UserProfileInfo

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta():
        model=User
        fields = ('username','email','password')

class TransactionForm(forms.ModelForm):
    transaction_name = forms.CharField()
    #amount = forms.IntField()
    #number of people



    class Meta():
        #model=Transact
        #fields=('transaction_name','amount', '')
#class UserProfileInfoForm(forms.ModelForm):
   # class Meta():
      #  model=UserProfileInfoFormfields=('portfolio_site','profile_pic')
