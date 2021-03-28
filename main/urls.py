from django import contrib
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', include('tweets.urls')),
    path('authenticate/', include('user_profile.urls')),
    path('admin/', admin.site.urls),
]
