from django.db import models
from user_profile.models import User


class Tweets(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.CharField(max_length=160)
    created = models.DateTimeField(auto_now_add=True)
    country = models.CharField(max_length=30)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        verbose_name_plural = 'Tweets'
        
    def __str__(self):
        return str(self.user)
    