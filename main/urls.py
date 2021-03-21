from django.contrib import admin
from django.urls import path, include
from tweets import views

urlpatterns = [
    path('', views.Index.as_view(), name='index'),
    path('admin/', admin.site.urls),
]
