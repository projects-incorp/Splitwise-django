from django.db import models
from django.contrib.auth.models import User

# Create your models here.
#class UserProfileInfo(models):
#    user = models.OnetoOneField(User)
#profile_pic=models.ImageField(upload_to='profile_pics'blank=True)
def __str__(self):
        # Built-in attribute of django.contrib.auth.models.User !
        username=self.user.username
        return self.user.username

#class Transact(models.Model):

class Transaction_Pairs(models.Model):
    person1=models.CharField(max_length=264)
    person2=models.CharField(max_length=264)
    amount=models.FloatField()


    def __str__(self):
        return self.person1 +" "+self.person2 + " "

class Transaction_history(models.Model):
    #Transaction_Pairs=models.ForeignKey(Transaction_Pairs,on_delete=models.CASCADE)
    date=models.DateField()
    reason=models.CharField(max_length=264)
    amount=models.FloatField()
    def __str__(self):
        return self.reason
