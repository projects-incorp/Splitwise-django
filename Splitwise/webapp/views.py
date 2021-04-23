from django.shortcuts import render
from webapp.forms import UserForm
from webapp.forms import TransactionForm
from webapp.models import Transaction_Pairs
#from webapp.forms import UserProfileInfo
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate,login,logout

#import all the views eg-from django.view.generic import(TemplateView,ListView)

def index(request):
    return render(request,'webapp/index.html')

@login_required
def special(request):
    return HttpResponse("You are logged in")

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))


def register(request):

    registered=False

    if request.method == "POST":
        user_form=UserForm(data=request.POST)
        #profile_form=UserProfileInfoForm(data=reuest.Post)
        if user_form.is_valid():
            #and profile_frm.is_valid()
            user =user_form.save()
            user.set_password(user.password)
            user.save()
            #profile=profile_form.save(commit=False)
            #profile.user=user
            #if 'profile_pic' in request.files:
                #profile.profile_pic=request.FILES['profile_pic']
            #profile.save
            registered=True

            #print(profile_forms.errors)
    else:
        user_form=UserForm()
        #profile_form=UserProfileInfoFrom()
    return render(request,'webapp/registeration.html',{'user_form':user_form,'registered':registered})
    #add key value pair 'profile_form':profile_form,

def user_login(request):

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username,password=password)

        if user:
            if user.is_active:
                login(request,user)
                return HttpResponseRedirect(reverse('index'))

            else:
                return HttpResponse("ACCOUNT NOT ACTIVE")

        else:
            print("Someone tried to login and failed!")
            print("Username: {} and password: {}".format(username,password))
            return HttpResponse("Invalid login details supplied!")

    else:
        return render(request, 'webapp/login.html', {})


def transaction(request):
    numpeople=0
    amt=0
    progress=False
    if request.method == "POST":
        transact_form=TransactionForm(data=request.POST)
        if transact_form.is_valid():
            #transact =transact_form.save()
            progress=True
            person1_=request.user.get_username()
            person2_=request.POST["person2"] #Replaced by the Friends Strings BY SHREYA
            amt=request.POST["amount"]
            amt1=float(amt)
            numpeople=request.POST["number_of_people"]
            numpeople_=int(numpeople)
            for i in range(1,numpeople_):
                contrib=(amt1)/float(numpeople)
                t_pair_count = Transaction_Pairs.objects.filter(person1=person1_,person2=person2_).count()
                print (t_pair_count)
                if t_pair_count==1:
                    obj=Transaction_Pairs.objects.get(person1=person1_,person2=person2_)
                    amt_=float(obj.amount)
                    amt_+=contrib
                    obj.amount=amt_
                    obj.save()
                    t_pair_count=0
                elif t_pair_count==0:
                    transact=Transaction_Pairs(person1=person1_,person2=person2_,amount=amt)
                    transact.save()
                    t_pair_count=0
                else:
                    break



            #Put in database

    else:
        transact_form=TransactionForm()
        return render(request,'webapp/transaction.html',{'transact_form':transact_form,'progress':progress})

    return render(request,'webapp/index.html',{'transact_form':transact_form,'progress':progress})





# Create your views here.
#For every page we need to Create
#class Name(TemplateView)
#template_name='name.html'
#etc etc
