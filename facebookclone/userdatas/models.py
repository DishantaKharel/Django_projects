from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class UserProfile(models.Model):

    user        = models.ForeignKey(User, on_delete= models.CASCADE)
    profile_pic = models.ImageField(upload_to='profile', default="profile/defaultprofile.jpg")
    bio         = models.TextField(max_length= 100, null= True, blank= True)
    timestamp   = models.DateTimeField(auto_now_add=True)


    def __str__(self):

        return self.user.username


    class Meta:

        ordering = ['-timestamp']


class UserPost(models.Model):

    user        = models.ForeignKey(User, on_delete=models.CASCADE)
    feed_photo  = models.ImageField(upload_to='images', null= True, blank= True)
    status      = models.TextField(max_length= 100, null= True, blank= True)
    timestamp   = models.DateTimeField(auto_now_add=True)


    def __str__(self):

        return self.user.username


    class Meta:

        ordering = ['-timestamp']