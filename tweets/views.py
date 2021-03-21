from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import View

from user_profile.models import User
from .models import Tweets


class Index(View):
    def get(self, request):
        
        context = {}
        return render(request, 'base.html', context)
    

class Profile(View):
    def get(self, request, username):
        user = User.objects.get(username=username)
        tweets = Tweets.objects.filter(user=user)
        context = {'user': user, 'tweets': tweets}
        return render(request, 'tweets/profile.html', context)

        