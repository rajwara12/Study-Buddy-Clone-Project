from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


class User(AbstractUser):
    name=models.CharField(max_length=50, null=True)
    bio = models.TextField( null=True)
    email = models.EmailField(unique=True, null=True)
    avatar = models.ImageField(  null=True,default="avatar.svg")

    # USERNAME_FIELD= 'email'
    REQUIRED_FIELDS=[]


class Topic(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self)  :
        return self.name


class Room(models.Model):
    host=models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    topic= models.ForeignKey(Topic, on_delete=models.SET_NULL, null=True)
    participants=models.ManyToManyField(User,related_name='participants')
    name = models.CharField(max_length=100) 
    description = models.TextField()
    updated_at= models.DateTimeField(auto_now=True)
    created_at  = models.DateTimeField(auto_now_add= True)

    class Meta:
        ordering = ['-updated_at','-created_at']


    def __str__(self)  :
        return self.name
    

class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE ) 
    room =models.ForeignKey(Room,on_delete=models.CASCADE)
    msg_body = models.TextField()
    updated_at= models.DateTimeField(auto_now=True)
    created_at  = models.DateTimeField(auto_now_add= True)     

    def __str__(self)  :
        return self.msg_body[:50]

    class Meta:
        ordering = ['-updated_at','-created_at']
    