from django.db import models
from django.contrib.auth.models import User

class UserFollower(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    count = models.IntegerField(default=1)
    followers = models.ManyToManyField(User, related_name='followers')
    
    def __str__(self):
        return self.user, str(self.count)
    
class Invitation(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField()
    code = models.CharField(max_length=20)
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    
    def __str__(self):
        return f'{self.sender.username}, {self.email}'
    