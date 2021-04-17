from django.shortcuts import render
from webapp.forms import UserForm
from webapp.forms import UserProfileInfo

def index(request):
    return render(request,'webapp/index.html')

def register(request):

    registered=False

    if request.method == "POST":
        user_form=UserForm(data=reuest.Post)
        #profile_form=UserProfileInfoForm(data=reuest.Post)
        if user_form.isvalid(): #and profile_frm.is_valid()
            user =user_form.save()
            user.set_password(user.password)
            user.save()
            #profile=profile_form.save(commit=False)
            #profile.user=user
            #if 'profile_pic' in request.files:
                #profile.profile_pic=request.FILES['profile_pic']
            #profile.save
            registered=True
         else:
             print(user_form.errors)
             #print(profile_forms.errors)
                 
    else:
        user_form=UserForm()
        #profile_form=UserProfileInfoFrom()
    return render(request,'webap/registeration.html',{'user_form':user_form,'registered':registered})
    #add key value pair 'profile_form':profile_form,

            



# Create your views here.
