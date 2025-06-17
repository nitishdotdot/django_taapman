from django.db import models
class userInfo(models.Model):
    first_name=models.CharField(max_length=20,null=False,blank=False)
    last_name=models.CharField(max_length=20,null=False,blank=False)
    email=models.EmailField(max_length=50,null=False,blank=False)
    password=models.CharField(max_length=50,null=False,blank=False)
    
