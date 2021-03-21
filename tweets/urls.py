from django.urls import path

from . import views
urlpatterns = [
    path('', views.Index.as_view(), name='index'),
    path('user/<str:username>/', views.Profile.as_view(), name='profile'),
    path('hashtag/<str:hashtag>/', views.HashTagCloud.as_view(), name='hashtag'),
    path('user/<str:username>/post/', views.PostTweet.as_view(), name='post_tweet'),
    path('search/', views.Search.as_view(), name='search_tweet'),
]
