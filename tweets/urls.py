from django.urls import path

from . import views
urlpatterns = [
    path('', views.Index.as_view(), name='index'),
    path('user/<str:username>/', views.Profile.as_view(), name='profile'),
    path('hashtag/<str:hashtag>/', views.HashTagCloud.as_view(), name='hashtag'),
    path('user/<str:username>/post/', views.PostTweet.as_view(), name='post_tweet'),
    path('search/', views.Search.as_view(), name='search_tweet'),
    path('search/hashtag/', views.SearchHashTag.as_view(), name='search_hashtag'),
    path('hashtag.json', views.HashTagJson.as_view()),
    path('profile/', views.UserRedirect.as_view()),
    path('most_followed/', views.MostFollowedUsers.as_view(), name='most_followed'),
]
