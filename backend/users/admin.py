from django.contrib import admin
from django.contrib.admin import register
from django.contrib.auth.admin import UserAdmin

from users.models import Follow, User 


class UserAdmin(UserAdmin):

    list_display = [
        'pk',
        'username',
        'email',
        'first_name',
        'last_name',
    ]
    list_filter = [
        'email',
        'username',
    ]

@register(Follow)
class FollowAdmin(admin.ModelAdmin):
    list_display = [
        'pk',
        'author',
        'user',
    ]
    list_filter = [
        'author',
        'user',
    ]

admin.site.register(User, UserAdmin)