from django.contrib import admin
from .models import *

class TweetAdmin(admin.ModelAdmin):
    list_display = ['user', 'text', 'created']
    list_filter = ['created',]
    ordering = ['-created',]
    search_fields = ['text',]
    
class HashTagAdmin(admin.ModelAdmin):
    list_display = ['name',]   

admin.site.register(Tweets, TweetAdmin)
admin.site.register(HashTag, HashTagAdmin)
