from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

from users.models import User

MIN_AMOUNT = 1
MAX_AMOUNT = 32000


class Tag(models.Model):
    """Модель тегов."""

    name = models.CharField(
        max_length=200,
        verbose_name='Название'
    )

    color = models.CharField(
        max_length=7,
        verbose_name='Цвет в HEX'
    )

    slug = models.SlugField(
        max_length=200,
        unique=True,
        verbose_name='Уникальный слаг'
    )

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'
        ordering = ['name']

    def __str__(self) -> str:
        return self.name


class Recipe(models.Model):
    """Модель рецептов."""

    tags = models.ManyToManyField(
        Tag,
        verbose_name='Список id тегов'
    )

    name = models.CharField(
        max_length=200,
        verbose_name='Название'
    )

    cooking_time = models.PositiveSmallIntegerField(
        verbose_name='Время приготовления (в минутах)',
        validators=[
            MinValueValidator(
                MIN_AMOUNT,
                message='Время приготовления не менее 1 минуты'),
            MaxValueValidator(
                MAX_AMOUNT,
                message='Время приготовления не может быть бесконечным'
            )
        ]
    )

    text = models.TextField(
        verbose_name='Описание'
    )

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор',
        related_name='recipes',

    )

    ingredients = models.ManyToManyField(
        'Ingredient',
        through='RecipeIngredient',
        verbose_name='Список ингредиентов',
        related_name='recipes',
    )

    image = models.ImageField(
        verbose_name='Картинка, закодированная в Base64',
        upload_to='recipes/images/',
    )

    pub = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата публикации'
    )

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'
        ordering = ['-pub']

    def __str__(self) -> str:
        return self.name


class Ingredient(models.Model):
    """Модель ингредиентов."""

    name = models.CharField(
        max_length=200,
        verbose_name='Название ингредиента'
    )

    measurement_unit = models.CharField(
        max_length=200,
        verbose_name='Единицы измерения'
    )

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'
        ordering = ['name']

    def __str__(self) -> str:
        return self.name


class RecipeIngredient(models.Model):
    """Модель количества ингредиентов для рецепта."""

    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        verbose_name='Рецепт',
        related_name='ingredient_list',
    )

    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        verbose_name='Ингредиент',
        related_name='ingredient_list',
    )

    amount = models.PositiveSmallIntegerField(
        verbose_name='Количество ингредиента',
        validators=[
            MinValueValidator(
                MIN_AMOUNT,
                message='Время приготовления не менее 1 минуты'),
            MaxValueValidator(
                MAX_AMOUNT,
                message='Время приготовления не может быть бесконечным'
            )
        ]
    )

    class Meta:
        verbose_name = 'Количество ингредиента'
        verbose_name_plural = 'Список ингредиентов'
        ordering = ['-amount']

    def __str__(self) -> str:
        return f'{self.recipe}, {self.ingredient}, {self.amount}'


class ShoppingCart(models.Model):
    """Модель списка покупок ингредиентов."""

    user = models.ForeignKey(
        User,
        verbose_name='Пользователь',
        on_delete=models.CASCADE,
        related_name='shopping_cart',
    )

    recipe = models.ForeignKey(
        Recipe,
        verbose_name='Рецепт',
        on_delete=models.CASCADE,
        related_name='is_in_shopping_cart',

    )

    class Meta:
        verbose_name = 'Список покупок'
        verbose_name_plural = 'Список покупок'
        ordering = ['recipe']

    def __str__(self):
        return (f'Пользователь {self.user} добавил {self.recipe}'
                'в список покупок')


class Favorite(models.Model):
    """Модель избранных рецептов."""

    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='is_favorited',
    )

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='favorites',

    )

    class Meta:
        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранное'
        ordering = ['recipe']

    def __str__(self):
        return (f'Пользователь {self.user} добавил {self.recipe} '
                'в избранное')
