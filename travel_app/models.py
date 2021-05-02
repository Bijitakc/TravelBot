from django.db import models
from django.contrib.auth.models import User
from django.utils.six import python_2_unicode_compatible


# Create your models here.


class Place(models.Model):
    title = models.CharField(max_length=100)
    desc = models.TextField()
    image = models.ImageField(upload_to='img')

    def __str__(self):
        return self.title

class BotMessage(models.Model):
    #A room for people to chat in.
    botinputs=models.TextField()
    #used for replies and saving to db
    id=models.AutoField(primary_key=True)


    def __str__(self):
        return self.botinputs

class BotReply(models.Model):
    botoutputs=models.TextField()
    id=models.AutoField(primary_key=True)


    def __str__(self):
        return self.botoutputs 
