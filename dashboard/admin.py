from django.contrib import admin
from .models import Follow, Follower, Friend_request, Friend, Friendship

# Register your models here.
admin.site.register(Follow)
admin.site.register(Follower)
admin.site.register(Friend_request)
admin.site.register(Friend)
admin.site.register(Friendship)