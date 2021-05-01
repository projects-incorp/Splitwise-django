from django.shortcuts import render
from webapp.forms import UserForm

from webapp.forms import TransactionForm
from webapp.forms import TransactionHistory
from webapp.models import Transaction_Pairs
from webapp.models import Transaction_history
#from webapp.forms import UserProfileInfo
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate,login,logout

#import all the views eg-from django.view.generic import(TemplateView,ListView)
def index(request):
    global person_n
    datap= Transaction_Pairs.objects.filter(person1=request.user.get_username())
    dataopp= Transaction_Pairs.objects.filter(person2=request.user.get_username())

    if request.GET.get('mybtn') or request.GET.get('mybtn1')  and person_n !="":
        amtr=int(request.GET.get('mytextbox'))
        obj=(Transaction_Pairs.objects.get(person1=request.user.get_username(),person2=person_n,) if Transaction_Pairs.objects.filter(person1=person_n,person2=request.user.get_username()).count()==0 else Transaction_Pairs.objects.get(person1=person_n,person2=request.user.get_username()))
        if request.GET.get('mybtn') and amtr!=0 and obj.amount!=0:
            #last if is so the value doesnt go from money owed 0 to negative
            obj.amount-=amtr
        elif request.GET.get('mybtn') and amtr==0:
            return HttpResponse("Enter an amount!") #I want it to be an alert

        elif request.GET.get('mybtn1'):
            obj.amount=0
        obj.save()



        datap= Transaction_Pairs.objects.filter(person1=request.user.get_username())
        dataopp= Transaction_Pairs.objects.filter(person2=request.user.get_username())
        person_n=""

    return render(request,'webapp/index.html',{"datap":datap,"dataopp":dataopp})

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
        #profile_form=UserProfileInfoForm(datap=reqest.Post)
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
            progress=True
            person1_=request.user.get_username()
            reason=request.POST["reason"]
            date=request.POST["date"]
            amt=request.POST["amount"]
            amt1=float(amt)
            people=request.POST["people"]
            user_list=[]
            a=0
            for x in range(0,len(people)):
                if people[x]==',':
                    temp=people[a:x]
                    a=x + 1
                    user_list.append(temp)
                    temp=""
            user_list.append(people[a:])
            numpeople_=len(user_list)+1
            for i in range(1,numpeople_):
                person2_=user_list[i-1]
                contrib=(amt1)/float(numpeople_)
                t_pair_count = Transaction_Pairs.objects.filter(person1=person1_,person2=person2_).count() + Transaction_Pairs.objects.filter(person1=person2_,person2=person1_).count()
                if t_pair_count==1:
                    #obj=(Transaction_Pairs.objects.get(person1=request.user.get_username(),person2=person2_,) if Transaction_Pairs.objects.filter(person1=person2_,person2=request.user.get_username()).count()==0 else Transaction_Pairs.objects.get(person1=person2_,person2=request.user.get_username()))
                    if Transaction_Pairs.objects.filter(person1=person2_,person2=request.user.get_username()).count()==0:
                        obj=Transaction_Pairs.objects.get(person1=request.user.get_username(),person2=person2_,)
                        flag=1
                    else:
                        obj=Transaction_Pairs.objects.get(person1=person2_,person2=request.user.get_username())
                        flag=0
                    if flag==1:
                        famt1=float(obj.amount)
                    elif flag==0:
                        famt1=-float(obj.amount)
                    amt_=float(obj.amount)
                    if flag==1:
                        amt_+=contrib
                        obj.amount=amt_
                    elif flag==0:
                        famt1+=contrib
                        obj.amount=famt1*(-1.0)
                        if obj.amount<0:
                            temp=obj.person1
                            obj.person1=obj.person2
                            obj.person2=temp
                            obj.amount=famt1

                    obj.save()

                    t_pair_count=0
                elif t_pair_count==0:
                    transact=Transaction_Pairs(person1=person1_,person2=person2_,amount=contrib)
                    transact.save()
                    t_pair_count=0
                else:
                    break
                history=Transaction_history(person1=person1_,person2=person2_,date=date,reason=reason,amount=contrib)
                history.save()



    else:
        transact_form=TransactionForm()

        return render(request,'webapp/transaction.html',{'transact_form':transact_form,'progress':progress,})
    datap= Transaction_Pairs.objects.filter(person1=request.user.get_username())
    dataopp= Transaction_Pairs.objects.filter(person2=request.user.get_username())
    return render(request,'webapp/index.html',{'transact_form':transact_form,'progress':progress,"datap":datap,'dataopp':dataopp})


person_n=""
def history(request):
    global person_n

    datah=Transaction_history.objects.filter(person1=request.user.get_username())
    dataopp= Transaction_history.objects.filter(person2=request.user.get_username())
    if request.method == 'POST':
        transact_history=TransactionHistory(data=request.POST)

        if transact_history.is_valid():
            person_n=request.POST["person_name"]

    else:
        transact_history=TransactionHistory()
        return render(request,'webapp/history.html',{'transact_history':transact_history,"datah":datah,"dataopp":dataopp})

    datah=Transaction_history.objects.filter(person1=request.user.get_username(),person2=person_n)
    dataopp= Transaction_history.objects.filter(person2=request.user.get_username(),person1=person_n)
    if Transaction_Pairs.objects.filter(person1=person_n,person2=request.user.get_username()).count()==0:
        famt1=Transaction_Pairs.objects.get(person1=request.user.get_username(),person2=person_n,)
        flag=True
<<<<<<< HEAD
    elif Transaction_Pairs.objects.filter(person1=request.user.get_username(),person2=person_n).count()==0:
        famt1=Transaction_Pairs.objects.get(person1=person_n,person2=request.user.get_username())
        flag=False
    else:
        return HttpResponse("Could not find Person")
=======
    else:
        famt1=Transaction_Pairs.objects.get(person1=person_n,person2=request.user.get_username())
        flag=False

>>>>>>> 8fe9857712a94934f07692ca9983158f84e6960d
    #famt1=(Transaction_Pairs.objects.get(person1=request.user.get_username(),person2=person_n,) and flag=1)
    if flag==True:
        famt=float(famt1.amount)
    elif flag==False:
        famt=-float(famt1.amount)
    return render(request,'webapp/history.html',{"flag":flag, "dataopp":dataopp,"person_n":person_n,"famount":famt,"datah":datah,"transact_history":transact_history})

'''
def nullify(request):
    global person_n
    print("HI1")
    if request.method == 'GET':
        print("HI2")
        obj=(Transaction_Pairs.objects.get(person1=request.user.get_username(),person2=person_n,) if Transaction_Pairs.objects.filter(person1=person_n,person2=request.user.get_username()).count()==0 else Transaction_Pairs.objects.get(person1=person_n,person2=request.user.get_username()))
        obj.amount=0
        obj.save()
        datap= Transaction_Pairs.objects.filter(person1=request.user.get_username())
        dataopp= Transaction_Pairs.objects.filter(person2=request.user.get_username())
        return render(request,'webapp/index.html',{"datap":datap,"dataopp":dataopp})
    else:
        return render(request,'webapp/index.html',{"datap":datap,"dataopp":dataopp})
'''

def settle(request):
<<<<<<< HEAD
    if request.method=='GET':
        c1=Transaction_Pairs.objects.filter(person1=request.user.get_username()).count()
        c2=Transaction_Pairs.objects.filter(person2=request.user.get_username()).count()
        if c1>0 and c2==0:
            obj1=Transaction_Pairs.objects.filter(person1=request.user.get_username())
            for i in obj1:
                obj2=obj1.exclude(person2=i.person2)
                counter1=Transaction_Pairs.objects.filter(person1=i.person2).count()
                counter2=Transaction_Pairs.objects.filter(person2=i.person2).count()
                check=0
                if counter1 > 0:
                    obj3=Transaction_Pairs.objects.filter(person1=i.person2)
                    obj3=obj3.exclude(person2=i.person1)
                if counter2 > 0:
                    check=1
                    obj3=Transaction_Pairs.objects.filter(person2=i.person2)
                    obj3=obj3.exclude(person1=i.person1)
                for j in obj2:
                    for k in obj3:
                        if(check==1):
                            if(j.person2==k.person1):
                                if(j.amount==k.amount):
                                    print("Entered")
                                    temp_amount=j.amount
                                    j.amount=0
                                    k.amount=0
                                    i.amount+=temp_amount
                                    i.save()
                                    j.save()
                                    k.save()
                        if(check==0):
                            if(j.person2==k.person2):
                                if(j.amount==k.amount):
                                    print("Entered")
                                    temp_amount=j.amount
                                    j.amount=0
                                    k.amount=0
                                    i.amount+=temp_amount
                                    i.save()
                                    j.save()
                                    k.save()
        if c1>0 and c2>0:
            obj1=Transaction_Pairs.objects.filter(person2=request.user.get_username())
            obj2=Transaction_Pairs.objects.filter(person1=request.user.get_username())
            for i in obj1:
                for j in obj2:
                    if(i.amount==j.amount):
                        temp_amount=i.amount
                        i.amount=0
                        j.amount=0
                        obj3=Transaction_Pairs.objects.filter(person1=i.person1,person2=j.person2)
                        for k in obj3:
                            k.amount+=temp_amount
                            i.save()
                            j.save()
                            k.save()
        if c2>0 and c1==0:
            obj1=Transaction_Pairs.objects.filter(person2=request.user.get_username())
            for i in obj1:
                obj2=obj1.exclude(person1=i.person1)
                for j in obj2:
                    obj3=Transaction_Pairs.objects.filter(person1=i.person1,person2=j.person1)
                    for k in obj3:
                        if(j.amount==k.amount):
                            temp_amount=j.amount
                            j.amount=0
                            k.amount=0
                            i.amount+=temp_amount
                            i.save()
                            j.save()
                            k.save()
=======
    def settle(request):
        if request.method=='GET':
            c1=Transaction_Pairs.objects.filter(person1=request.user.get_username()).count()
            c2=Transaction_Pairs.objects.filter(person2=request.user.get_username()).count()
            if c1>0 and c2==0:
                obj1=Transaction_Pairs.objects.filter(person1=request.user.get_username())
                for i in obj1:
                    obj2=obj1.exclude(person2=i.person2)
                    counter1=Transaction_Pairs.objects.filter(person1=i.person2).count()
                    counter2=Transaction_Pairs.objects.filter(person2=i.person2).count()
                    check=0
                    if counter1 > 0:
                        obj3=Transaction_Pairs.objects.filter(person1=i.person2)
                        obj3=obj3.exclude(person2=i.person1)
                    if counter2 > 0:
                        check=1
                        obj3=Transaction_Pairs.objects.filter(person2=i.person2)
                        obj3=obj3.exclude(person1=i.person1)
                    for j in obj2:
                        for k in obj3:
                            if(check==1):
                                if(j.person2==k.person1):
                                    if(j.amount==k.amount):
                                        print("Entered")
                                        temp_amount=j.amount
                                        j.amount=0
                                        k.amount=0
                                        i.amount+=temp_amount
                                        i.save()
                                        j.save()
                                        k.save()
                            if(check==0):
                                if(j.person2==k.person2):
                                    if(j.amount==k.amount):
                                        print("Entered")
                                        temp_amount=j.amount
                                        j.amount=0
                                        k.amount=0
                                        i.amount+=temp_amount
                                        i.save()
                                        j.save()
                                        k.save()
            if c1>0 and c2>0:
                obj1=Transaction_Pairs.objects.filter(person2=request.user.get_username())
                obj2=Transaction_Pairs.objects.filter(person1=request.user.get_username())
                for i in obj1:
                    for j in obj2:
                        if(i.amount==j.amount):
                            temp_amount=i.amount
                            i.amount=0
                            j.amount=0
                            obj3=Transaction_Pairs.objects.filter(person1=i.person1,person2=j.person2)
                            for k in obj3:
                                k.amount+=temp_amount
                                i.save()
                                j.save()
                                k.save()
            if c2>0 and c1==0:
                obj1=Transaction_Pairs.objects.filter(person2=request.user.get_username())
                for i in obj1:
                    obj2=obj1.exclude(person1=i.person1)
                    for j in obj2:
                        obj3=Transaction_Pairs.objects.filter(person1=i.person1,person2=j.person1)
                        for k in obj3:
                            if(j.amount==k.amount):
                                temp_amount=j.amount
                                j.amount=0
                                k.amount=0
                                i.amount+=temp_amount
                                i.save()
                                j.save()
                                k.save()
>>>>>>> 8fe9857712a94934f07692ca9983158f84e6960d

        datap= Transaction_Pairs.objects.filter(person1=request.user.get_username())
        dataopp= Transaction_Pairs.objects.filter(person2=request.user.get_username())
        return render(request, 'webapp/index.html',{'datap':datap,'dataopp':dataopp})
