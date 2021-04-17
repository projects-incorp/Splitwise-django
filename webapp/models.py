from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class UserProfileInfo(models):
    user = models.OnetoOneField(User)

#profile_pic=models.ImageField(upload_to='profile_pics'blank=True)

    