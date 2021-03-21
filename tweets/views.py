from django.http.response import HttpResponseRedirect
from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import View

from user_profile.models import User
from .models import HashTag, Tweets
from .forms import TweetForm

class Index(View):
    def get(self, request):
        
        context = {}
        return render(request, 'base.html', context)
    

class Profile(View):
    def get(self, request, username):
        user = User.objects.get(username=username)
        tweets = Tweets.objects.filter(user=user)
        form = TweetForm(self.request.POST or None)
        context = {'user': user, 'tweets': tweets, 'form': form}
        return render(request, 'tweets/profile.html', context)

        
class PostTweet(View):
    def post(self, request, username):
        form = TweetForm(self.request.POST)
        if form.is_valid():
            user = User.objects.get(username=username)
            tweet = Tweets(text=form.cleaned_data['text'], user=user, country=form.cleaned_data['country'])
            tweet.save()
            words = form.cleaned_data['text'].split(' ')
            for word in words:
                if word[0] == '#':
                    hashtag, created = HashTag.objects.get_or_create(name=word[1:])
                    hashtag.tweet.add(tweet)
                return HttpResponseRedirect('profile'+username)
            

class HashTagCloud(View):
    def get(self, request, hashtag):
        hastag = HashTag.objects.get(name=hashtag)
        context = {'tweets': hashtag.tweet}
        return render(request, 'hastag.html', context)