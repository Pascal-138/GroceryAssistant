from django.db.models import Sum
from django.shortcuts import HttpResponse, get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from djoser.views import UserViewSet
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from .filters import IngredientNameFilter, RecipeFilter
from .pagination import CustomPagination
from .serializers import (IngredientSerializer, RecipeSerializer,
                          RecipeCreateSerializer, RecipeShortSerializer,
                          TagSerializer, CustomUserSerializer,
                          CustomUserCreateSerializer,
                          FollowCreateSerializer, FollowSerializer)
from recipes.models import (Favorite, Ingredient, Recipe, RecipeIngredient,
                            ShoppingCart, Tag)
from users.models import Follow, User


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    pagination_class = None
    permission_classes = [AllowAny, ]


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    pagination_class = None
    permission_classes = [AllowAny, ]
    search_fields = ['^name', ]
    filter_backends = [IngredientNameFilter, ]


class RecipeViewSet(ModelViewSet):
    queryset = Recipe.objects.all()
    pagination_class = CustomPagination
    filter_backends = [DjangoFilterBackend, ]
    filterset_class = RecipeFilter

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return RecipeSerializer
        return RecipeCreateSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @action(
        detail=True,
        methods=['POST', 'DELETE'],
    )
    def favorite(self, request, pk):
        recipe_obj = get_object_or_404(Recipe, pk=pk)
        if request.method == 'POST':
            already_existed, created = Favorite.objects.get_or_create(
                user=request.user,
                recipe=recipe_obj
            )
            if not created:
                return Response(
                    {'errors': 'Ошибка при создании записи.'},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            serializer = RecipeShortSerializer(recipe_obj,
                                               context={'request': request})
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        elif request.method == 'DELETE':
            try:
                favorite = Favorite.objects.get(user=request.user,
                                                recipe=recipe_obj)
                favorite.delete()
                return Response(
                    {'message': 'Рецепт удален из избранного.'},
                    status=status.HTTP_204_NO_CONTENT,
                )
            except Favorite.DoesNotExist:
                return Response(
                    {'errors': 'Рецепт не найден в избранном.'},
                    status=status.HTTP_400_BAD_REQUEST,
                )

    @action(
        detail=True,
        methods=['POST', 'DELETE'],
    )
    def shopping_cart(self, request, pk=None):
        recipe = self.get_object()
        user = self.request.user

        if request.method == 'POST':
            if ShoppingCart.objects.filter(recipe=recipe, user=user).exists():
                return Response(
                    {'errors': 'Рецепт уже добавлен'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            ShoppingCart.objects.create(recipe=recipe, user=user)
            serializer = RecipeSerializer(recipe)
            return Response(
                data=serializer.data,
                status=status.HTTP_201_CREATED
            )

        obj = get_object_or_404(ShoppingCart, recipe=recipe, user=user)
        obj.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(
        detail=False,
        methods=['GET'],
        url_path='download_shopping_cart',
        permission_classes=[IsAuthenticated, ]
    )
    def download_shopping_cart(self, request):
        ingredient_list = "Cписок покупок:"
        ingredients = RecipeIngredient.objects.filter(
            recipe__is_in_shopping_cart__user=request.user
        ).values(
            'ingredient__name', 'ingredient__measurement_unit'
        ).annotate(amount_sum=Sum('amount'))
        for num, i in enumerate(ingredients):
            ingredient_list += (
                f"\n{i['ingredient__name']} - "
                f"{i['amount_sum']} {i['ingredient__measurement_unit']}"
            )
            if num < ingredients.count() - 1:
                ingredient_list += ', '
        file = 'shopping_list'
        response = HttpResponse(
            ingredient_list,
            'Content-Type: application/txt'
        )
        response['Content-Disposition'] = f'attachment; filename="{file}.txt"'
        return response


class CustomUserViewSet(UserViewSet):
    serializer_class = CustomUserSerializer
    permission_classes = (IsAuthenticated,)

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CustomUserCreateSerializer
        return self.serializer_class


class FollowViewSet(viewsets.ModelViewSet):

    queryset = Follow.objects.all()
    serializer_class = FollowSerializer
    permission_classes = (IsAuthenticated,)
    # pagination_class = CustomPagination

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(
        methods=['GET'],
        detail=False,)
    def subscriptions(self, request):
        subscriptions = self.get_queryset().select_related('following')
        serializer = FollowSerializer(subscriptions,
                                      many=True,
                                      context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(
        detail=True,
        methods=['POST', 'DELETE'],
    )
    def subscribe(self, request, pk=None):
        author = get_object_or_404(User, pk=pk).pk
        user = request.user.pk

        data = {
            'user': request.user.pk,
            'author': pk
        }

        if request.method == 'POST':
            serializer = FollowCreateSerializer(data=data)
            serializer.is_valid()
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        elif request.method == 'DELETE':
            if not Follow.objects.filter(user=user, author=author).exists():
                return Response(
                    {'errors': 'Вы не подписаны'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            follow = Follow.objects.get(user=user, author=author)
            follow.delete()
            return Response(
                {'message': 'Подписка удалена'},
                status=status.HTTP_204_NO_CONTENT
            )
