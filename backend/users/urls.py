# from rest_framework import routers
# from django.urls import path, include

# from users.views import FollowViewSet, UserViewSet

# app_name = 'users'

# router = routers.DefaultRouter()
# router.register(r'users', UserViewSet)
# router.register(r'subscriptions', FollowViewSet, basename='subscriptions')



# urlpatterns = [
#     path('users/subscriptions/', FollowViewSet.as_view()),
#     path('auth/', include('djoser.urls.authtoken')),
#     path('', include(router.urls))  
# ]
