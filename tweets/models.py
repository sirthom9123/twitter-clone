from django.db import models
from django.contrib.auth.models import User


class Tweets(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_profile')
    text = models.CharField(max_length=160)
    created = models.DateTimeField(auto_now_add=True)
    country = models.CharField(max_length=30)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        verbose_name_plural = 'Tweets'
        
    def __str__(self):
        return str(self.user)
    
    
class HashTag(models.Model):
    name = models.CharField(max_length=80, unique=True)
    tweet = models.ManyToManyField(Tweets)
    
    
    def __str__(self):
        return self.name
    