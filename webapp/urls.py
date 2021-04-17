from django.conf.urls import path
from webapp import views

app_name='webapp'

urlpattern=[
    path('register/'views.register,name='register')


]