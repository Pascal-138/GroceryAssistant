# #from django.db import transaction
# from rest_framework import serializers

# from djoser.serializers import UserCreateSerializer, UserSerializer
# from users.models import User, Follow
# from recipes.models import Recipe
# from api.serializers import RecipeDetailsSerializer


# class CustomUserSerializer(UserSerializer):
#     """Сериализатор для модели User."""

#     is_subscribed = serializers.SerializerMethodField()

#     class Meta:
#         model = User
#         fields = [
#             'id',
#             'email',
#             'username',
#             'first_name',
#             'last_name',
#             'is_subscribed',
#         ]

#     def get_is_subscribed(self, obj):
#         request = self.context.get('request')
#         if request.user.is_anonymous:
#             return False
#         return Follow.objects.filter(
#             user=request.user,
#             author=obj,
#         ).exists()


# class CustomUserCreateSerializer(UserCreateSerializer):
#     """Сериализатор для регистрации новых пользователей."""

#     #username = serializers.CharField (source='username')

#     class Meta:
#         model = User
#         fields = [
#             'email',
#             'id',
#             'username',
#             'first_name',
#             'last_name',
#             'password',
#         ]


# class FollowSerializer(serializers.ModelSerializer):
#     """Сериализатор для подписок."""

#     id = serializers.ReadOnlyField(source='author.id')
#     username = serializers.ReadOnlyField(source='author.username')
#     email = serializers.ReadOnlyField(source='author.email')
#     first_name = serializers.ReadOnlyField(source='author.first_name')
#     last_name = serializers.ReadOnlyField(source='author.last_name')
#     is_subscribed = serializers.SerializerMethodField(
#         method_name='get_is_subscribed')
#     recipes = serializers.SerializerMethodField(method_name='get_recipes')
#     recipes_count = serializers.SerializerMethodField(method_name='get_recipes_count')  

#     class Meta:
#         model = Follow
#         fields = [
#             'email',
#             'id',
#             'username',
#             'first_name',
#             'last_name',
#             'is_subscribed',
#             'recipes',
#             'recipes_count',
#         ]

#     def get_recipes_count(self, obj):
#         recipes = Recipe.objects.filter(author=obj.author)
#         return recipes.count()

#     def get_is_subscribed(self, obj):
#         request = self.context.get('request')
#         if request.user.is_anonymous:
#             return False
#         return Follow.objects.filter(
#             user=request.user,
#             author=obj.author,
#         ).exists()

#     def get_recipes(self, obj):
#         request = self.context.get('request')
#         recipes = Recipe.objects.filter(author=obj.author)
#         limit = request.GET.get('recipes_limit')

#         if limit:
#             recipes = recipes[:int(limit)]
#         serializer = RecipeDetailsSerializer(recipes, many=True)
#         return serializer.data

