import json
from django.http.response import HttpResponseRedirect
from django.shortcuts import render
from django.template.loader import render_to_string
from django.http import HttpResponse
from django.views.generic import View
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth.models import User

from .models import HashTag, Tweets
from .forms import SearchForm, SearchHashTagForm, TweetForm
from user_profile.models import UserFollower
import logging
logger = logging.getLogger('django')

TWEET_PER_PAGE = 5


class LoginRequiredMixin(object):
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(LoginRequiredMixin, self).dispatch(*args, **kwargs)

class Index(View):
    def get(self, request):
        
        context = {'name': 'Django'}
        return render(request, 'base.html', context)

class UserRedirect(View):
    def get(self, request):
        if request.user.is_authenticated():
            logger.info('authorized user')
            return HttpResponseRedirect('/user/'+request.user.username)    
        else:
            logger.info('unauthorized user')
            return HttpResponseRedirect('login')
        
        
class Profile(View):
    def get(self, request, username):
        params = dict()
        userProfile = User.objects.get(username=username)
        try:
            userFollower = UserFollower.objects.get(user=userProfile)
            if userFollower.followers.filter(user=request.user.username).exists():
                params['following'] = True
            else:
                params['following'] = False
        except:
            userFollower = []
        
        tweets = Tweets.objects.filter(user=userProfile).order_by('-created')
        form = TweetForm(initial={'country': 'Global'})
        search_form = SearchForm()
        
        context = {
            'profile': userProfile, 
            'tweets': tweets, 
            'form': form, 
            'search_form': search_form
            }
        return render(request, 'tweets/profile.html', context)

    def post(self, request, username):
        follow = request.POST['follow']
        user = User.objects.get(username=request.user.username)
        userProfile = User.objects.get(username=username)
        userFollower, status = UserFollower.objects.get_or_create(user=userProfile)
        userFollower.count += 1
        userFollower.save()
        if follow == 'true':
            userFollower.followers.add(user)
        else:
            userFollower.followers.remove(user)
        return HttpResponse(json.dumps(""), content_type='apllication/json')
    
class MostFollowedUsers(View):
    def get(self, request):
        userFollowers = UserFollower.objects.order_by('-count')[:2]
        context = {'userFollowers': userFollowers}
        return render(request, 'tweets/users.html', context)    
        
class PostTweet(View):
    def post(self, request, username):
        form = TweetForm(self.request.POST or None)
        if form.is_valid():
            user = User.objects.get(username=username)
            tweet = Tweets(text=form.cleaned_data['text'], user=user, country=form.cleaned_data['country'])
            tweet.save()
            words = form.cleaned_data['text'].split(' ')
            for word in words:
                if word[0] == '#':
                    hashtag, created = HashTag.objects.get_or_create(name=word[1:])
                    hashtag.tweet.add(tweet)
                return HttpResponseRedirect('/user/'+username)
            

class HashTagCloud(View):
    def get(self, request, hashtag):
        hastag = HashTag.objects.get(name=hashtag)
        context = {'tweets': hashtag.tweet}
        return render(request, 'hastag.html', context)
    

class Search(View):
    def get(self, request):
        form = SearchForm()
        
        context ={'form': form}
        return render(request, 'tweets/search.html', context)
        
        
    def post(self, request):
        form = SearchForm(request.POST)
        if form.is_valid():
            query = form.cleaned_data['query']
            tweets = Tweets.objects.filter(text__icontains=query)
            context = {'query': query, 'tweets': tweets}
            return_str = render_to_string('partials/_tweets_search.html', context)
            return HttpResponse(json.dumps(return_str), content_type='application/json')
        else:
            return HttpResponseRedirect('search_tweet')
        
class SearchHashTag(View):
    def get(self, request):
        form = SearchHashTagForm()
        context = {'search': form}
        return render(request, 'search_hashtag.html', context)

    def post(self, request):
        query = request.POST['query']
        form = SearchHashTagForm()
        hashtags = HashTag.objects.filter(name__contains=query)
        context = {'hashtags': hashtags, 'search': form}
        return render(request, 'search_hashtag.html', context)


class HashTagJson(View):
    def get(self, request):
        query = request.GET['query']
        hashtaglist = []
        hashtags = HashTag.objects.filter(name__icontains=query)
        for hashtag in hashtags:
            temp = {'query': hashtag.name}
            hashtaglist.append(temp)
        return HttpResponse(json.dumps(hashtaglist), content_type="application/json")