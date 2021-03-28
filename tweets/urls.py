from django.urls import path
from django.views.decorators.cache import cache_page

from . import views
urlpatterns = [
    path('', views.Index.as_view(), name='index'),
    path('user/<str:username>/', views.Profile.as_view(), name='profile'),
    path('user/<str:username>/post/', views.PostTweet.as_view(), name='post_tweet'),
    path('hashtag/<str:hashtag>/', cache_page(60 * 15)(views.HashTagCloud.as_view()), name='hashtag'),
    path('search/', views.Search.as_view(), name='search_tweet'),
    path('search/hashtag/', views.SearchHashTag.as_view(), name='search_hashtag'),
    path('hashtag.json', views.HashTagJson.as_view()),
    path('profile/', views.UserRedirect.as_view()),
    path('most_followed/', views.MostFollowedUsers.as_view(), name='most_followed'),
]
