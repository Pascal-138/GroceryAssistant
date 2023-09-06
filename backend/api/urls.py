from django.urls import path, include
from rest_framework import routers
from api.views import (CustomUserViewSet, FollowMakeView, FollowViewSet,
                       IngredientViewSet, TagViewSet, RecipeViewSet)

app_name = 'api'

router = routers.DefaultRouter()

router.register('users/subscriptions', FollowViewSet)
router.register('users', CustomUserViewSet)
router.register('tags', TagViewSet)
router.register('recipes', RecipeViewSet)
router.register('ingredients', IngredientViewSet)


urlpatterns = [
    # path('users/<int:pk>/subscribe/', FollowViewSet.as_view(
    #     {'post': 'subscribe', 'delete': 'subscribe'})),
    path(
        'users/<int:user_id>/subscribe/',
        FollowMakeView.as_view(),
        name='subscribe'),
    path('', include(router.urls)),
    path('auth/', include('djoser.urls.authtoken')),
]
