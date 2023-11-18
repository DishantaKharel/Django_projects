from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Resources(models.Model):
    user = models.ForeignKey(User, on_delete= models.CASCADE)
    resource_name = models.CharField(max_length= 50)
    description = models.TextField(max_length= 100, null= True, blank= True)
    price = models.DecimalField(max_digits= 7, decimal_places= 3)
    resource_image = models.ImageField(upload_to='images')
    timestamp = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):

        return self.resource_name

    class Meta:

        ordering = ['-timestamp']