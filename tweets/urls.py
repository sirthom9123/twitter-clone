from django.urls import path

from . import views
urlpatterns = [
    path('', views.Index.as_view(), name='index'),
    path('user/<str:username>/', views.Profile.as_view(), name='profile'),
]
